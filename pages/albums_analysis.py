import streamlit as st
import pandas as pd
import yaml
import os
from streamlit_utils import plots, layouts, data_processing


layouts.set_page_layout()
st.sidebar.markdown("# **Albums Analysis** 📀️ ")

layouts.set_page_header("Albums Analysis", "📀️")

# with open('config/path_config.yaml', 'r') as config_file:
#     path_config = yaml.safe_load(config_file)

# data_dir = path_config['data_dir'][0]
# file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}
#
# albums_path = str(file_paths['albums.csv'])
# albums_table = pd.read_csv(albums_path, sep='~')
#
# playlists_path = str(file_paths['playlists.csv'])
# playlists_table = pd.read_csv(playlists_path, sep="~")
#
# artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
# artists_genres_full_unknown = pd.read_csv(artists_genres_full_unknown_path, sep='~')

data = data_processing.load_and_process_data('config/path_config.yaml')

playlists_table = data["playlists"]
artists_table = data["artists"]
tracks_table = data["tracks"]
albums_table = data["albums"]

st.subheader('Distribution of Album Popularity',)
plots.create_histogram(
            data=albums_table,
            x='Album Popularity',
        )

top_10_albums_popularity = (
    albums_table.nlargest(n=10, columns='Album Popularity')
    )
min_x = top_10_albums_popularity['Album Popularity'].min() - 3
max_x = top_10_albums_popularity['Album Popularity'].max()

merged_playlists_albums = pd.merge(
    top_10_albums_popularity,
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
    'Album Name': 'first',   # Keep the first occurrence of the track name
    'Artist Name': lambda x: ', '.join(x.dropna().unique()),  # Concatenate unique artist names, separated by commas
    'Album Popularity': 'first',
}).reset_index()

top_10_albums_artists_sorted = top_10_albums_artists_grouped.sort_values(by='Album Popularity', ascending=True)

st.subheader('Top 10 Most Popular Albums')
plots.create_bar_plot(
    data=top_10_albums_artists_sorted,
    x='Album Popularity',
    y='Album Name',
    orientation='h',
    text='Album Popularity',
    range_x=[min_x, max_x],
    hover_data={'Artist Name': True},
)

# The 'errors="coerce"' argument replaces invalid date entries with NaT (Not a Time),
# ensuring the column can be processed without raising errors for incorrect formats.
albums_table['Release Date'] = pd.to_datetime(albums_table['Release Date'], errors='coerce')

albums_table['release_month'] = albums_table['Release Date'].dt.month

monthly_releases = albums_table['release_month'].value_counts().reset_index()
monthly_releases.columns = ['Month', 'Release Count']

month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
monthly_releases['Month Name'] = monthly_releases['Month'].map(month_names)

monthly_releases = monthly_releases.sort_values(by='Month')

st.subheader('Seasonality of Album Releases')
plots.create_bar_plot(
    data=monthly_releases,
    x='Month Name',
    y='Release Count',
    text='Release Count',
    showticklabels=True,
)

albums_table['release_year'] = albums_table['Release Date'].dt.year

yearly_releases = albums_table['release_year'].value_counts().sort_index().reset_index()
yearly_releases.columns = ['Release Year', 'Release Count']

st.subheader('Album Releases Timeline')

plots.create_line_chart(
    data=yearly_releases,
    x='Release Year',
    y='Release Count',
    text='Release Count',
    yaxis_title='Number of Releases (log scale)',
    log_y=True,
)

st.subheader('Distribution of Album Types')
plots.create_pie_chart(
    data=albums_table,
    names='Album Type',
)
