import os
import yaml
import pandas as pd
import streamlit as st
from streamlit_utils import layouts, data_processing


layouts.set_page_layout()
st.sidebar.markdown("# **Data Preview** 🧮 ")

layouts.set_page_header("Data Preview", "🧮")

# with open('config/path_config.yaml', 'r') as config_file:
#     path_config = yaml.safe_load(config_file)

# data_dir = path_config['data_dir'][0]
# file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}
#
# playlists_path = str(file_paths['playlists.csv'])
# albums_path = str(file_paths['albums.csv'])
# artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
# tracks_path = str(file_paths['tracks.csv'])
#
# playlists_table = pd.read_csv(playlists_path, sep="~")
# albums_table = pd.read_csv(albums_path, sep='~')
# artists_genres_full_unknown = pd.read_csv(artists_genres_full_unknown_path, sep='~')
# tracks_table = pd.read_csv(tracks_path, sep='~')
#
# playlists_table = data_processing.rename_playlists(playlists_table)
#
# albums_table = data_processing.rename_albums(albums_table)
#
# artists_table = data_processing.rename_artists(artists_genres_full_unknown)
#
# tracks_table = data_processing.rename_tracks(tracks_table)
#
data = data_processing.load_and_process_data('config/path_config.yaml')

playlists_table = data["playlists"]
artists_table = data["artists"]
tracks_table = data["tracks"]
albums_table = data["albums"]

total_playlists = playlists_table['Playlist ID'].nunique()
average_followers = playlists_table['Playlist Total Followers'].mean()
total_unique_tracks = playlists_table['Track ID'].nunique()

max_followers_playlist = playlists_table.sort_values(by='Playlist Total Followers', ascending=False).iloc[0]
min_followers_playlist = playlists_table.sort_values(by='Playlist Total Followers').iloc[0]

st.subheader("Playlists Analysis - Overview Statistics")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.metric(label="🎶 Total Playlists", value=total_playlists)
        st.caption("The total number of playlists analyzed.")

with col2:
    with st.container(border=True):
        st.metric(label="👥 Avg. Followers/Playlist", value=f"{average_followers:,.0f}")
        st.caption("Average number of followers across all playlists.")

st.divider()

st.subheader("Playlists:")

tab1_playlists, tab2_playlists = st.tabs(["Data", "Descriptive Statistics"])

with tab1_playlists:
    st.dataframe(playlists_table, width=1200, height=210, hide_index=True)
with tab2_playlists:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        max_followers = playlists_table['Playlist Total Followers'].max()
        most_followed_playlist = playlists_table.loc[
            playlists_table['Playlist Total Followers'].idxmax(), 'Country'
        ]
        avg_followers = playlists_table['Playlist Total Followers'].mean()

        st.metric(label="🏆 Most Followers", value=f"{max_followers:,.0f}")
        st.metric(label="🎶 Playlist with Most Followers", value=most_followed_playlist)

    with col2:
        total_tracks = len(playlists_table['Track ID'])
        unique_tracks = playlists_table['Track ID'].nunique()

        st.metric(label="🎵 Total Tracks", value=total_tracks)
        st.metric(label="🎵 Unique Tracks", value=unique_tracks)

    with col3:
        total_artists = len(playlists_table['Artist ID'])
        unique_artists = playlists_table['Artist ID'].nunique()

        st.metric(label="🎤 Total Artists", value=total_artists)
        st.metric(label="🎤 Unique Artists", value=unique_artists)

    with col4:
        total_albums = len(playlists_table['Album ID'])
        unique_albums = playlists_table['Album ID'].nunique()

        st.metric(label="💿 Total Albums", value=total_albums)
        st.metric(label="💿 Unique Albums", value=unique_albums)

st.subheader("Albums:")
tab1_albums, tab2_albums = st.tabs(["Data", "Descriptive Statistics"])
with tab1_albums:
    st.dataframe(albums_table, width=1200, height=210, hide_index=True)
with tab2_albums:
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_popularity = albums_table['Album Popularity'].mean()
        max_popularity = albums_table['Album Popularity'].max()

        st.metric(label="🔥 Avg. Album Popularity", value=f"{avg_popularity:.1f}")
        st.metric(label="🎉 Max Album Popularity", value=max_popularity)

    with col2:
        avg_tracks = albums_table['Total Tracks'].mean()
        max_tracks = albums_table['Total Tracks'].max()

        st.metric(label="🎵 Avg. Tracks/Album", value=f"{avg_tracks:.0f}")
        st.metric(label="🎵 Max Tracks/Album", value=max_tracks)

    with col3:
        earliest_release = albums_table['Release Date'].min()
        latest_release = albums_table['Release Date'].max()

        st.metric(label="📅 Earliest Release", value=earliest_release)
        st.metric(label="📅 Latest Release", value=latest_release)

st.subheader("Artists:")
tab1_artists, tab2_artists = st.tabs(["Data", "Descriptive Statistics"])
with tab1_artists:
    st.dataframe(artists_table, width=1200, height=210, hide_index=True)
with tab2_artists:
    col1, col2 = st.columns(2)

    with col1:
        avg_popularity = artists_table['Artist Popularity'].mean()
        most_popular_artist = artists_table.loc[artists_table['Artist Popularity'].idxmax(), 'Artist Name']
        max_popularity = artists_table['Artist Popularity'].max()

        st.metric(label="🔥 Avg. Artist Popularity", value=f"{avg_popularity:.1f}")
        st.metric(label="🏆 Most Popular Artist", value=most_popular_artist)
        st.metric(label="🎉 Max Artist Popularity", value=max_popularity)

    with col2:
        avg_followers_artist = artists_table['Artist Total Followers'].mean()
        max_followers = artists_table['Artist Total Followers'].max()
        most_followed_artist = artists_table.loc[artists_table['Artist Total Followers'].idxmax(), 'Artist Name']

        st.metric(label="👥 Avg. Followers/Artist", value=f"{avg_followers_artist:,.0f}")
        st.metric(label="🏅 Most Followed Artist", value=most_followed_artist)
        st.metric(label="🌟 Max Followers", value=f"{max_followers:,.0f}")

st.subheader("Tracks:")
tab1_tracks, tab2_tracks = st.tabs(["Data", "Descriptive Statistics"])
with tab1_tracks:
    st.dataframe(tracks_table, width=1200, height=210, hide_index=True)
with tab2_tracks:
    col1, col2 = st.columns(2)

    with col1:
        avg_popularity_track = tracks_table['Track Popularity'].mean()
        max_popularity_track = tracks_table['Track Popularity'].max()
        most_popular_track = tracks_table.loc[
            tracks_table['Track Popularity'].idxmax(), 'Track Name']
        max_popularity = tracks_table['Track Popularity'].max()

        st.metric(label="🔥 Avg. Track Popularity", value=f"{avg_popularity_track:.1f}")
        st.metric(label="🏆 Most Popular Track", value=most_popular_track)
        st.metric(label="🎉 Max Track Popularity", value=max_popularity_track)

    with col2:
        avg_duration = (tracks_table['Duration (ms)'].mean() / 60000).round(2)
        max_duration = (tracks_table['Duration (ms)'].max() / 60000).round(2)
        min_duration = (tracks_table['Duration (ms)'].min() / 60000).round(2)

        st.metric(label="⏱️ Avg. Duration (min)", value=f"{avg_duration}")
        st.metric(label="⏳ Max Duration (min)", value=f"{avg_duration}")
        st.metric(label="⏱️ Min Duration (min)", value=f"{avg_duration}")
