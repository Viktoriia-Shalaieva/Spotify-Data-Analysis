import os

import pandas as pd
import streamlit as st

from streamlit_utils import plots
from source import utils


@st.cache_data
def load_data(path_config):
    """
    Load data files specified in the configuration.

    This function reads CSV files for playlists, albums, tracks, and artists from
    the paths defined in the provided configuration dictionary.

    Args:
        path_config (dict): A configuration dictionary containing:
            - 'data_dir' (list): A list with the directory path for data files.
            - 'files_names' (dict): A dictionary of file names with keys matching
              'playlists.csv', 'albums.csv', 'tracks.csv', and 'artists_full.csv'.
    """
    data_dir = path_config['data_dir'][0]
    file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

    playlists_path = str(file_paths['playlists.csv'])
    albums_path = str(file_paths['albums.csv'])
    tracks_path = str(file_paths['tracks.csv'])
    artists_full_path = str(file_paths['artists_full.csv'])

    playlists = pd.read_csv(playlists_path, sep="~")
    albums = pd.read_csv(albums_path, sep='~')
    artists_full = pd.read_csv(artists_full_path, sep='~')
    tracks = pd.read_csv(tracks_path, sep='~')

    return {
        "playlists": playlists,
        "artists": artists_full,
        "tracks": tracks,
        "albums": albums,
    }


@st.cache_data
def process_data(data):
    """Process and standardize data by renaming columns in each dataset."""
    processed_data = {
        "playlists": rename_playlists(data['playlists']),
        "artists": rename_artists(data['artists']),
        "tracks": rename_tracks(data['tracks']),
        "albums": rename_albums(data['albums'])
    }
    return processed_data


@st.cache_data
def load_and_process_data(config_path):
    """
    Load, process, and standardize data from the provided configuration.

    This function loads configuration details, retrieves data from specified file paths,
    and processes the data by renaming columns for consistency across datasets.
    """
    path_config = utils.load_config(config_path)
    data = load_data(path_config)
    return process_data(data)


@st.cache_data
def rename_playlists(dataframe):
    """Rename columns in the playlists DataFrame for consistency and readability."""
    return dataframe.rename(columns={
        'playlist_id': 'Playlist ID',
        'playlist_name': 'Playlist Name',
        'country': 'Country',
        'playlist_followers_total': 'Playlist Total Followers',
        'track_id': 'Track ID',
        'album_id': 'Album ID',
        'artist_id': 'Artist ID'
    })


@st.cache_data
def rename_artists(dataframe):
    """Rename columns in the artists DataFrame for consistency and readability."""
    return dataframe.rename(columns={
        'artist_id': 'Artist ID',
        'artist_name': 'Artist Name',
        'artist_followers': 'Artist Total Followers',
        'artist_genres': 'Artist Genres',
        'artist_popularity': 'Artist Popularity'
    })


@st.cache_data
def rename_tracks(dataframe):
    """Rename columns in the tracks DataFrame for consistency and readability."""
    return dataframe.rename(columns={
        'track_id': 'Track ID',
        'track_name': 'Track Name',
        'track_duration_ms': 'Duration (ms)',
        'track_explicit': 'Explicit Content',
        'track_popularity': 'Track Popularity'
    })


@st.cache_data
def rename_albums(dataframe):
    """Rename columns in the albums DataFrame for consistency and readability."""
    return dataframe.rename(columns={
        'album_id': 'Album ID',
        'album_name': 'Album Name',
        'album_type': 'Album Type',
        'album_release_date': 'Release Date',
        'album_total_tracks': 'Total Tracks',
        'album_label': 'Label',
        'album_popularity': 'Album Popularity'
    })


@st.cache_data
def load_country_coords(file_path):
    """
    Load country coordinates and return a DataFrame for mapping.

    This function reads a configuration file containing country names and their
    coordinates (latitude and longitude) and transforms the data into a pandas DataFrame.
    """
    country_coords = utils.load_config(file_path)

    countries_for_map = []
    latitudes = []
    longitudes = []

    for country, coords in country_coords['countries'].items():
        countries_for_map.append(country)
        latitudes.append(coords['latitude'])
        longitudes.append(coords['longitude'])

    return pd.DataFrame({
        'Country': countries_for_map,
        'Latitude': latitudes,
        'Longitude': longitudes
    })


def classify_genres_detailed_structure(genre, all_genres_with_subgenres):
    """
    Classifies a genre into a parent genre based on a given mapping.

    Args:
        genre (str): The genre to classify.
        all_genres_with_subgenres (dict): A dictionary mapping parent genres to their subgenres.

    Returns:
        str: The parent genre if found, otherwise 'Other'.
    """
    for parent_genre, subgenres in all_genres_with_subgenres.items():
        if genre in subgenres:
            return parent_genre
    return 'Other'


def classify_other_genres(genre, additional_genres):
    """Classifies a genre into a parent genre based on additional genres mapping."""
    for parent_genre, subgenres in additional_genres.items():
        if subgenres is not None and genre in subgenres:
            return parent_genre
    return 'Other'


def expand_and_classify_artists_genres(artists_table):
    """
    Expand and classify artist genres into parent genres.

    This function processes an artist genres table by:
    - Splitting the 'Artist Genres' column into individual genres.
    - Cleaning genre strings by removing special characters and converting them to lowercase.
    - Classifying each genre into a parent genre based on predefined genre structures.
    """
    all_genres_with_subgenres = utils.load_config('./data/genres/genres.yaml')
    additional_genres_with_subgenres = utils.load_config('./data/genres/additional_genres.yaml')
    artists_table['Artist Genres'] = artists_table['Artist Genres'].str.split(', ')

    expanded_artists_genres = artists_table.explode('Artist Genres')

    # r"[\"\'\[\]]": Regular expression to match the characters.
    # regex=True : Indicates using a regular expression for matching.
    expanded_artists_genres['Artist Genres'] = (expanded_artists_genres['Artist Genres']
                                                .str.replace(r"[\"\'\[\]]", '', regex=True))

    expanded_artists_genres['Artist Genres'] = expanded_artists_genres['Artist Genres'].str.lower()

    expanded_artists_genres['Artist Genres'] = (
        expanded_artists_genres['Artist Genres']
        .str.replace(r'&\s*country', 'country', regex=True)
    )
    expanded_artists_genres['Parent Genre'] = (
        expanded_artists_genres['Artist Genres']
        .apply(lambda genre: classify_genres_detailed_structure(genre, all_genres_with_subgenres))
    )
    expanded_artists_genres['Parent Genre'] = expanded_artists_genres.apply(
        lambda row: classify_other_genres(row['Artist Genres'], additional_genres_with_subgenres)
        if row['Parent Genre'] == 'Other' else row['Parent Genre'],
        axis=1
    )
    return expanded_artists_genres


def prepare_median_popularity_data(playlists_table, tracks_table):
    """
    Merges playlist and track data, calculates the median track popularity by country,
    and returns the merged table along with a list of countries sorted by median popularity.
    """
    merged_playlists_tracks = pd.merge(
        playlists_table,
        tracks_table,
        on='Track ID',
        how='left'
    )
    median_popularity = (
        merged_playlists_tracks
        .groupby('Country')['Track Popularity']
        .median()
    )
    median_popularity_df = median_popularity.reset_index()

    median_popularity_df.columns = ['Country', 'Median Popularity']

    median_popularity_df = median_popularity_df.sort_values(by='Median Popularity', ascending=False)

    sorted_countries = median_popularity_df['Country'].tolist()
    return {
        'merged_playlists_tracks': merged_playlists_tracks,
        'sorted_countries': sorted_countries
    }


def calculate_std_dev_ranges_and_percentages(data):
    """
    Calculate standard deviation ranges and percentages for a dataset.

    This function computes the mean, median, and standard deviation of the input data.
    It then calculates ranges within 1, 2, and 3 standard deviations from the mean,
    and determines the percentage of data points that fall within each range.

    Args:
        data (pd.Series): A pandas Series containing numerical data.

    Returns:
        tuple: A tuple containing three dictionaries:
            - `popularity_stats`: Contains basic statistics:
                - 'mean': Mean of the data.
                - 'median': Median of the data.
                - 'std': Standard deviation of the data.
            - `std_ranges`: Contains the lower and upper bounds for 1, 2, and 3 standard deviations:
                - '1_std': (lower_bound, upper_bound)
                - '2_std': (lower_bound, upper_bound)
                - '3_std': (lower_bound, upper_bound)
            - `perc_within_std`: Contains the percentage of data points within each range:
                - 'within_1_std': Percentage within 1 standard deviation.
                - 'within_2_std': Percentage within 2 standard deviations.
                - 'within_3_std': Percentage within 3 standard deviations.
    """
    mean_value = data.mean()
    median_value = data.median()
    std_value = data.std()
    total_values = len(data)

    popularity_stats = {
        "mean": mean_value,
        "median": median_value,
        "std": std_value
    }

    std_ranges = {}
    perc_within_std = {}

    for i in range(1, 4):
        lower_bound = mean_value - i * std_value
        upper_bound = mean_value + i * std_value

        std_ranges[f'{i}_std'] = (lower_bound, upper_bound)

        within_range = len(data[(data >= lower_bound) & (data <= upper_bound)])
        perc_within_std[f'within_{i}_std'] = within_range / total_values * 100

    return popularity_stats, std_ranges, perc_within_std


def prepare_top_tracks_data(playlists_table, tracks_table, artists_table):
    """
    Identify the top 10 most frequent tracks from the playlists table, enriches them with details from
    the tracks and artists tables, and aggregates artist names for each track.
    """
    # Count tracks and select top 10
    track_frequencies = playlists_table['Track ID'].value_counts().reset_index()
    # track_frequencies.columns = ['Track ID', 'Frequency']
    top_10_tracks = track_frequencies.nlargest(n=10, columns='count')

    # Merge with tracks and artists data
    top_tracks_with_details = top_10_tracks.merge(
        tracks_table[['Track ID', 'Track Name', 'Track Popularity', 'Explicit Content']],
        on='Track ID',
        how='left'
    )
    tracks_with_artists = top_tracks_with_details.merge(
        playlists_table[['Track ID', 'Artist ID']],
        on='Track ID',
        how='left'
    )
    unique_tracks_with_artists = tracks_with_artists.drop_duplicates(subset=['Track ID'])
    unique_tracks_with_artists.loc[:, 'Artist ID'] = unique_tracks_with_artists['Artist ID'].str.split(', ')
    exploded_tracks_with_artists = unique_tracks_with_artists.explode('Artist ID')

    tracks_with_artist_names = exploded_tracks_with_artists.merge(
        artists_table[['Artist ID', 'Artist Name']],
        on='Artist ID',
        how='left'
    )

    # Group data by track and aggregate values
    grouped_tracks_data = tracks_with_artist_names.groupby('Track ID').agg({
        'Track Name': 'first',  # Keep the first occurrence of the track name
        'Artist Name': lambda x: ', '.join(x.dropna().unique()),  # Concatenate unique artist names, separated by commas
        'count': 'first',
        'Track Popularity': 'first',
        'Explicit Content': 'first'
    }).reset_index()

    tracks_summary = grouped_tracks_data[
        ['Track Name', 'Artist Name', 'count', 'Track Popularity', 'Explicit Content']]
    tracks_summary.columns = ['Track Name', 'Artists', 'Frequency in Playlists', 'Popularity', 'Explicit']

    return tracks_summary


def prepare_top_artists_data(playlists_table, artists_table):
    """
    Identify the top 10 most frequent artists from the playlists table and their presence in playlists.

    Returns:
        dict: Contains:
            - 'artist_per_playlist' (pd.DataFrame): A DataFrame showing how often each
              artist appears in playlists for each country.
            - 'top_10_artists_full' (pd.DataFrame): A DataFrame containing information on the top 10 artists.
    """
    playlists_table['Artist ID'] = playlists_table['Artist ID'].str.split(', ')

    # Expand the playlists table so that each artist in the 'artist_id' list gets its own row
    expanded_playlists_artists = playlists_table.explode('Artist ID')

    # Group by country and artist_id to count how often each artist appears in playlists for each country
    artist_per_playlist = (
        expanded_playlists_artists
        .groupby('Country')['Artist ID']
        .value_counts()
        .reset_index()
    )
    artist_counts = expanded_playlists_artists['Artist ID'].value_counts().reset_index()

    top_10_artists = artist_counts.nlargest(n=10, columns='count')

    top_10_artists_full = top_10_artists.merge(
        artists_table[['Artist ID', 'Artist Name', 'Artist Total Followers', 'Artist Popularity', 'Artist Genres']],
        on='Artist ID',
        how='left'
    )
    top_10_artists_full = top_10_artists_full[
        ['Artist Name', 'count', 'Artist Total Followers', 'Artist Popularity', 'Artist Genres']
    ]
    top_10_artists_full.columns = ['Artist Name', 'Number of songs in playlists',
                                   'Followers', 'Artist Popularity', 'Artist Genres']

    return {
        'artist_per_playlist': artist_per_playlist,
        'top_10_artists_full': top_10_artists_full,
    }


def process_tracks_data(playlists_table, tracks_table, artists_table):
    """
    Process track data to create detailed information about tracks and their artists.

    Returns:
        dict: Contains:
            - 'top_10_tracks': Top 10 tracks sorted by popularity.
            - 'grouped_tracks': Grouped track data with artist names, track duration in minutes and additional columns.
    """
    merged_playlists_tracks = pd.merge(
        playlists_table[['Track ID', 'Artist ID']],
        tracks_table,
        on='Track ID',
        how='left'
    )

    merged_playlists_tracks.loc[:, 'Artist ID'] = merged_playlists_tracks['Artist ID'].str.split(', ')
    expanded_tracks_artists = merged_playlists_tracks.explode('Artist ID')

    tracks_artists_name = expanded_tracks_artists.merge(
        artists_table[['Artist ID', 'Artist Name']],
        on='Artist ID',
        how='left'
    )

    tracks_artists_grouped = tracks_artists_name.groupby('Track ID').agg({
        'Track Name': 'first',  # Keep the first occurrence of the track name
        'Artist Name': lambda x: ', '.join(x.dropna().unique()),  # Concatenate unique artist names, separated by commas
        'Duration (ms)': 'first',
        'Explicit Content': 'first',
        'Track Popularity': 'first',
    }).reset_index()

    top_10_tracks_by_popularity = (
        tracks_artists_grouped.nlargest(n=10, columns='Track Popularity')
        .sort_values(by='Track Popularity', ascending=True)
    )

    tracks_artists_grouped['Explicit Status'] = (
        tracks_artists_grouped['Explicit Content']
        .map({True: 'Explicit', False: 'Non-Explicit'})
    )

    tracks_artists_grouped['Track Duration (minutes)'] = tracks_artists_grouped['Duration (ms)'] / 60000

    return {
        'top_10_tracks': top_10_tracks_by_popularity,
        'grouped_tracks': tracks_artists_grouped,
    }


def format_number_text(column):
    """
    Format numeric values in a column into human-readable text.

    Converts numbers into abbreviated text format with 'K' for thousands and 'M' for millions.
    Numbers below 1,000 remain unchanged.
    """
    return column.apply(
        lambda x: (
            f"{x / 1e6:.1f}M" if x >= 1e6 else
            f"{x / 1e3:.1f}K" if x >= 1e3 else
            str(x)
        )
    )


def process_artists_data(artists_table):
    """
    Process artist data to determine the top 10 artists by popularity
    and total followers. It also categorizes artists into follower groups and
    calculates the distribution of these groups.

    Returns:
        dict: Contains:
            - 'top_10_artists_by_popularity': Top 10 artists by popularity.
            - 'top_10_artists_by_followers': Top 10 artists by total followers, including a formatted followers column.
            - 'bin_counts_followers': Distribution of artists by follower count groups.
    """
    top_10_artists_by_popularity = (
        artists_table.nlargest(n=10, columns='Artist Popularity')
        .sort_values(by='Artist Popularity', ascending=True)
    )

    top_10_artists_by_followers = (
        artists_table.nlargest(n=10, columns='Artist Total Followers')
        .sort_values(by='Artist Total Followers', ascending=True)
    )

    top_10_artists_by_followers['Artist Total Followers (formatted)'] = (
        format_number_text(
            top_10_artists_by_followers['Artist Total Followers']
        )
    )

    artists_table['Follower Group'] = pd.cut(
        artists_table['Artist Total Followers'],
        bins=[0, 1e6, 5e6, 10e6, 50e6, 100e6, 150e6],
        labels=['<1M', '1-5M', '5-10M', '10-50M', '50-100M', '>100M'],
        ordered=True
    )

    bin_counts_followers = artists_table['Follower Group'].value_counts(sort=False)

    return {
        'top_10_artists_by_popularity': top_10_artists_by_popularity,
        'top_10_artists_by_followers': top_10_artists_by_followers,
        'bin_counts_followers': bin_counts_followers
    }


def process_albums_data(albums_table, playlists_table, artists_table):
    """
        Process album data to analyze popularity, release patterns, and artist associations.

        This function processes album data to identify the top 10 most popular albums,
        analyze seasonality and timeline trends in album releases, and associate albums
        with their respective artists.

        Returns:
            dict: Contains:
            - 'top_10_albums_by_popularity' (pd.DataFrame): Top 10 albums by popularity.
            - 'top_10_albums_artists_sorted' (pd.DataFrame): Top 10 albums with artist names.
            - 'monthly_releases' (pd.DataFrame): Monthly album release counts.
            - 'yearly_releases' (pd.DataFrame): Yearly album release counts.
            - 'albums_table' (pd.DataFrame): Updated with release month and year columns.
        """
    # For Top 10 Most Popular Albums
    top_10_albums_by_popularity = (
        albums_table.nlargest(n=10, columns='Album Popularity')
    )

    merged_playlists_albums = pd.merge(
        top_10_albums_by_popularity,
        playlists_table[['Album ID', 'Artist ID']],
        on='Album ID',
        how='left'
    )
    merged_playlists_albums.loc[:, 'Artist ID'] = merged_playlists_albums['Artist ID'].str.split(', ')
    expanded_albums_artists = merged_playlists_albums.explode('Artist ID')

    albums_artists_name = expanded_albums_artists.merge(
        artists_table[['Artist ID', 'Artist Name']],
        on='Artist ID',
        how='left'
    )

    top_10_albums_artists_grouped = albums_artists_name.groupby('Album ID').agg({
        'Album Name': 'first',  # Keep the first occurrence of the track name
        'Artist Name': lambda x: ', '.join(x.dropna().unique()),  # Concatenate unique artist names, separated by commas
        'Album Popularity': 'first',
    }).reset_index()

    # For Top 10 Most Popular Albums
    top_10_albums_artists_sorted = top_10_albums_artists_grouped.sort_values(by='Album Popularity', ascending=True)

    # The 'errors="coerce"' argument replaces invalid date entries with NaT (Not a Time),
    # ensuring the column can be processed without raising errors for incorrect formats.
    albums_table['Release Date'] = pd.to_datetime(albums_table['Release Date'], errors='coerce')

    albums_table['release_month'] = albums_table['Release Date'].dt.month

    # For Seasonality of Album Releases
    monthly_releases = albums_table['release_month'].value_counts().reset_index()
    monthly_releases.columns = ['Month', 'Release Count']

    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    monthly_releases['Month Name'] = monthly_releases['Month'].map(month_names)

    monthly_releases = monthly_releases.sort_values(by='Month')

    # For Distribution of Album Types
    albums_table['release_year'] = albums_table['Release Date'].dt.year

    # For Album Releases Timeline
    yearly_releases = albums_table['release_year'].value_counts().sort_index().reset_index()
    yearly_releases.columns = ['Release Year', 'Release Count']

    return {
        'top_10_albums_by_popularity': top_10_albums_by_popularity,
        'top_10_albums_artists_sorted': top_10_albums_artists_sorted,
        'monthly_releases': monthly_releases,
        'yearly_releases': yearly_releases,
        'albums_table': albums_table
    }
