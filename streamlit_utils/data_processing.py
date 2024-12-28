import os
import yaml
import pandas as pd
import streamlit as st


def load_config(config_path, encoding='utf-8'):
    with open(config_path, 'r', encoding=encoding) as file:
        return yaml.safe_load(file)


@st.cache_data
def load_data(path_config):
    data_dir = path_config['data_dir'][0]
    file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

    playlists_path = str(file_paths['playlists.csv'])
    albums_path = str(file_paths['albums.csv'])
    artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
    tracks_path = str(file_paths['tracks.csv'])

    playlists = pd.read_csv(playlists_path, sep="~")
    albums = pd.read_csv(albums_path, sep='~')
    artists = pd.read_csv(artists_genres_full_unknown_path, sep='~')
    tracks = pd.read_csv(tracks_path, sep='~') if 'albums.csv' in file_paths else None

    return {
        "playlists": playlists,
        "artists": artists,
        "tracks": tracks,
        "albums": albums
    }


def process_data(data):
    processed_data = {
        "playlists": rename_playlists(data['playlists']),
        "artists": rename_artists(data['artists']),
        "tracks": rename_tracks(data['tracks']),
        "albums": rename_albums(data['albums'])
    }
    return processed_data


@st.cache_data
def load_and_process_data(config_path):
    path_config = load_config(config_path)
    data = load_data(path_config)
    return process_data(data)


def rename_playlists(dataframe):
    return dataframe.rename(columns={
        'playlist_id': 'Playlist ID',
        'playlist_name': 'Playlist Name',
        'country': 'Country',
        'playlist_followers_total': 'Playlist Total Followers',
        'track_id': 'Track ID',
        'album_id': 'Album ID',
        'artist_id': 'Artist ID'
    })


def rename_artists(dataframe):
    return dataframe.rename(columns={
        'artist_id': 'Artist ID',
        'artist_name': 'Artist Name',
        'artist_followers': 'Artist Total Followers',
        'artist_genres': 'Artist Genres',
        'artist_popularity': 'Artist Popularity'
    })


def rename_tracks(dataframe):
    return dataframe.rename(columns={
        'track_id': 'Track ID',
        'track_name': 'Track Name',
        'track_duration_ms': 'Duration (ms)',
        'track_explicit': 'Explicit Content',
        'track_popularity': 'Track Popularity'
    })


def rename_albums(dataframe):
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
    country_coords = load_config(file_path)

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
    for parent_genre, subgenres in all_genres_with_subgenres.items():
        if genre in subgenres:
            return parent_genre
    return 'Other'


def expand_and_classify_artists_genres(artists_table):
    all_genres_with_subgenres = load_config('./data/genres/genres.yaml')
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
    return expanded_artists_genres


def calculate_std_dev_ranges_and_percentages(data):
    mean_value = data.mean()
    median_value = data.median()
    std_value = data.std()
    total_values = len(data)

    summary_stats = {
        "mean": mean_value,
        "median": median_value,
        "std": std_value
    }

    std_dev_ranges = {}
    percentages_within_std_dev = {}

    for i in range(1, 4):
        lower_bound = mean_value - i * std_value
        upper_bound = mean_value + i * std_value

        std_dev_ranges[f'{i}_std_dev'] = (lower_bound, upper_bound)

        within_range = len(data[(data >= lower_bound) & (data <= upper_bound)])
        percentages_within_std_dev[f'within_{i}_std_dev'] = within_range / total_values * 100

    return summary_stats, std_dev_ranges, percentages_within_std_dev
