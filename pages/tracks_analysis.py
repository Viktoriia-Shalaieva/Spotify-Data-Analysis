import os
import yaml
import pandas as pd
import streamlit as st
from streamlit_utils import plots, layouts, data_processing


layouts.set_page_layout()
st.sidebar.markdown("**Tracks Analysis** 🎵")

layouts.set_page_header("Tracks Analysis", "🎵")


# with open('config/path_config.yaml', 'r') as config_file:
#     path_config = yaml.safe_load(config_file)
#
# data_dir = path_config['data_dir'][0]
# file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}
#
#
# @st.cache_data
# def load_playlists_data():
#     playlists_path = str(file_paths['playlists.csv'])
#     return pd.read_csv(playlists_path, sep="~")
#
#
# @st.cache_data
# def load_tracks_data():
#     tracks_path = str(file_paths['tracks.csv'])
#     return pd.read_csv(tracks_path, sep='~')
#
#
# @st.cache_data
# def load_artists_data():
#     artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
#     return pd.read_csv(artists_genres_full_unknown_path, sep='~')
#
#
# playlists_table = load_playlists_data()
# tracks_table = load_tracks_data()
# artists_genres_full_unknown = load_artists_data()
#
# playlists_table = data_processing.rename_playlists(playlists_table)
#
# artists_table = data_processing.rename_artists(artists_genres_full_unknown)
#
# tracks_table = data_processing.rename_tracks(tracks_table)


data = data_processing.load_and_process_data('config/path_config.yaml')

playlists_table = data["playlists"]
artists_table = data["artists"]
tracks_table = data["tracks"]

help_popularity = 'The value of popularity will be between 0 and 100, with 100 being the most popular'

st.subheader('Distribution of Track Popularity', help=help_popularity)
plots.create_histogram(
    data=tracks_table,
    x='Track Popularity',
)

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
    'Track Name': 'first',   # Keep the first occurrence of the track name
    'Artist Name': lambda x: ', '.join(x.dropna().unique()),  # Concatenate unique artist names, separated by commas
    'Duration (ms)': 'first',
    'Explicit Content': 'first',
    'Track Popularity': 'first',
}).reset_index()

top_10_tracks_popularity = (
    tracks_artists_grouped.nlargest(n=10, columns='Track Popularity')
    .sort_values(by='Track Popularity', ascending=True)
)

min_x = top_10_tracks_popularity['Track Popularity'].min() - 3
max_x = top_10_tracks_popularity['Track Popularity'].max()

st.subheader('Top 10 Most Popular Tracks', help=help_popularity)
plots.create_bar_plot(
    data=top_10_tracks_popularity,
    x='Track Popularity',
    y='Track Name',
    orientation='h',
    text='Track Popularity',
    range_x=[min_x, max_x],
    hover_data={'Artist Name': True},
)

tracks_artists_grouped['Explicit Status'] = (
    tracks_artists_grouped['Explicit Content']
    .map({True: 'Explicit', False: 'Non-Explicit'})
)

st.subheader('Distribution of Explicit and Non-Explicit Tracks')
plots.create_pie_chart(
    data=tracks_artists_grouped,
    names='Explicit Status',
)

st.subheader('Analysis of Track Popularity for Explicit and Non-Explicit Tracks', help=help_popularity)


tab1_boxplot, tab2_histogram = st.tabs(['Box Plot', 'Histogram'])

with tab1_boxplot:
    plots.create_boxplot(
        data=tracks_artists_grouped,
        x='Explicit Status',
        y='Track Popularity',
        color_discrete_map={
            'Explicit': 'red',
            'Non-Explicit': 'green'
        },
    )

with tab2_histogram:
    plots.create_histogram(
        data=tracks_artists_grouped,
        x='Track Popularity',
        color='Explicit Status',
        color_discrete_map={
            'Explicit': 'red',
            'Non-Explicit': 'green'
        },
    )

tracks_artists_grouped['Track Duration (minutes)'] = tracks_artists_grouped['Duration (ms)'] / 60000

help_trendline = ("""Trendlines show the overall relationship between track duration and popularity 
                  for Explicit and Non-Explicit tracks.""")

st.subheader('Relationship Between Track Duration and Popularity with Trendlines', help=help_trendline)
plots.create_scatter_plot(
    data=tracks_artists_grouped,
    x='Track Duration (minutes)',
    y='Track Popularity',
    color='Explicit Status',
    hover_data=['Track Name'],
    symbol='Explicit Status',
    color_map={
                'Explicit': 'red',
                'Non-Explicit': 'green'
            },
)

show_explanation = st.checkbox('Show explanation', value=False)

if show_explanation:
    st.info("""
        ### Track Popularity vs. Duration: Explanation
        This scatter plot visualizes the relationship between the **duration of tracks** (in minutes) and their 
        **popularity**. 
        - The tracks are categorized as **Explicit** (containing explicit content) or **Non-Explicit**.
        - Each dot represents a track, and the trendlines (red for Explicit, green for Non-Explicit) indicate the 
        general pattern of popularity changes with track duration.

        #### How to interpret:
        1. **Trendlines**: 
           - These lines show the overall trend for each category using the LOWESS (Locally Weighted Scatterplot 
           Smoothing) method.
           - They help identify patterns in the data without assuming a strict linear relationship.
           - For example, a rising trendline indicates that longer tracks in that category tend to be more popular.
        2. **Colors**:
           - Red dots and lines: Represent Explicit tracks.
           - Green dots and lines: Represent Non-Explicit tracks.
        3. **Key Observations**:
           - Look for patterns such as peaks or declines in popularity for specific durations.
           - Compare the trends between Explicit and Non-Explicit categories to identify differences in listener 
           preferences.
    """)
