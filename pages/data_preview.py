import streamlit as st
from modules.nav import navbar
from modules import components
import pandas as pd
import yaml
import os


components.set_page_layout()
st.sidebar.markdown("# **Data Preview** 🧮 ")

components.set_page_header("Data Preview", "🧮")

with open('config/path_config.yaml', 'r') as config_file:
    path_config = yaml.safe_load(config_file)

data_dir = path_config['data_dir'][0]
raw_dir = path_config['raw_dir'][0]
file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

playlists_path = str(file_paths['playlists.csv'])
albums_path = str(file_paths['albums.csv'])
artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
tracks_path = str(file_paths['tracks.csv'])

playlists_table = pd.read_csv(playlists_path, sep="~")
albums_table = pd.read_csv(albums_path, sep='~')
artists_genres_full_unknown = pd.read_csv(artists_genres_full_unknown_path, sep='~')
tracks_table = pd.read_csv(tracks_path, sep='~')

playlists_table = playlists_table.rename(columns={
    'playlist_id': 'Playlist ID',
    'playlist_name': 'Playlist Name',
    'country': 'Country',
    'playlist_followers_total': 'Total Followers',
    'track_id': 'Track ID',
    'album_id': 'Album ID',
    'artist_id': 'Artist ID'
})

albums_table = albums_table.rename(columns={
    'album_id': 'Album ID',
    'album_name': 'Album Name',
    'album_type': 'Album Type',
    'album_release_date': 'Release Date',
    'album_total_tracks': 'Total Tracks',
    'album_label': 'Label',
    'album_popularity': 'Popularity'
})

artists_table = artists_genres_full_unknown.rename(columns={
    'artist_id': 'Artist ID',
    'artist_name': 'Artist Name',
    'artist_followers': 'Total Followers',
    'artist_genres': 'Genres',
    'artist_popularity': 'Popularity'
})

tracks_table = tracks_table.rename(columns={
    'track_id': 'Track ID',
    'track_name': 'Track Name',
    'track_duration_ms': 'Duration (ms)',
    'track_explicit': 'Explicit Content',
    'track_popularity': 'Popularity'
})

playlists_table['Playlist ID'] = playlists_table['Playlist ID'].astype(str)
albums_table['Album ID'] = albums_table['Album ID'].astype(str)
artists_table['Artist ID'] = artists_table['Artist ID'].astype(str)
tracks_table['Track ID'] = tracks_table['Track ID'].astype(str)

total_playlists = playlists_table['Playlist ID'].nunique()
average_followers = playlists_table['Total Followers'].mean()
total_unique_tracks = playlists_table['Track ID'].nunique()

max_followers_playlist = playlists_table.sort_values(by='Total Followers', ascending=False).iloc[0]
min_followers_playlist = playlists_table.sort_values(by='Total Followers').iloc[0]

st.subheader("Playlists Analysis - Overview Statistics")

# st.metric(label="Total Number of Playlists", value=total_playlists)
# st.metric(label="Average Number of Followers per Playlist", value=f"{average_followers:.0f}")
# st.metric(label="Total Number of Unique Tracks", value=total_unique_tracks)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.metric(label="🎶 Total Playlists", value=total_playlists)
        st.caption("The total number of playlists analyzed.")

with col2:
    with st.container(border=True):
        st.metric(label="👥 Avg. Followers/Playlist", value=f"{average_followers:,.0f}")
        st.caption("Average number of followers across all playlists.")

with col3:
    with st.container(border=True):
        st.metric(label="🎵 Unique Tracks", value=total_unique_tracks)
        st.caption("Number of unique tracks included in the playlists.")

st.divider()

st.subheader("Playlists:")

tab1_playlists, tab2_playlists = st.tabs(["Data", "Descriptive Statistics"])

with tab1_playlists:
    st.dataframe(playlists_table, height=210,  hide_index=True)
with tab2_playlists:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        max_followers = playlists_table['Total Followers'].max()
        most_followed_playlist = playlists_table.loc[
            playlists_table['Total Followers'].idxmax(), 'Country'
        ]
        avg_followers = playlists_table['Total Followers'].mean()

        with st.container(border=True):
            st.metric(label="🏆 Most Followers", value=f"{max_followers:,.0f}")
            st.metric(label="🎶 Playlist with Most Followers", value=most_followed_playlist)

    with col2:
        total_tracks = len(playlists_table['Track ID'])
        unique_tracks = playlists_table['Track ID'].nunique()

        with st.container(border=True):
            st.metric(label="🎵 Total Tracks", value=total_tracks)
            st.metric(label="🎵 Unique Tracks", value=unique_tracks)

    with col3:
        total_artists = len(playlists_table['Artist ID'])
        unique_artists = playlists_table['Artist ID'].nunique()

        with st.container(border=True):
            st.metric(label="🎤 Total Artists", value=total_artists)
            st.metric(label="🎤 Unique Artists", value=unique_artists)

    with col4:
        total_albums = len(playlists_table['Album ID'])
        unique_albums = playlists_table['Album ID'].nunique()

        with st.container(border=True):
            st.metric(label="💿 Total Albums", value=total_albums)
            st.metric(label="💿 Unique Albums", value=unique_albums)

st.subheader("Albums:")
tab1_albums, tab2_albums = st.tabs(["Data", "Descriptive Statistics"])
with tab1_albums:
    st.dataframe(albums_table, width=1200, height=210, hide_index=True)
with tab2_albums:
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_popularity = albums_table['Popularity'].mean()
        max_popularity = albums_table['Popularity'].max()

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

    st.dataframe(albums_table.describe(), width=750)
    st.dataframe(albums_table.describe(include=['object']), width=750)

st.subheader("Artists:")
tab1_artists, tab2_artists = st.tabs(["Data", "Descriptive Statistics"])
with tab1_artists:
    st.dataframe(artists_table, width=1200, height=210, hide_index=True)
with tab2_artists:
    col1, col2 = st.columns(2)

    with col1:
        avg_popularity = artists_table['Popularity'].mean()
        most_popular_artist = artists_table.loc[artists_table['Popularity'].idxmax(), 'Artist Name']
        max_popularity = artists_table['Popularity'].max()

        st.metric(label="🔥 Avg. Artist Popularity", value=f"{avg_popularity:.1f}")
        st.metric(label="🏆 Most Popular Artist", value=most_popular_artist)
        st.metric(label="🎉 Max Artist Popularity", value=max_popularity)

    with col2:
        avg_followers_artist = artists_table['Total Followers'].mean()
        max_followers = artists_table['Total Followers'].max()
        most_followed_artist = artists_table.loc[artists_table['Total Followers'].idxmax(), 'Artist Name']

        st.metric(label="👥 Avg. Followers/Artist", value=f"{avg_followers_artist:,.0f}")
        st.metric(label="🌟 Max Followers", value=f"{max_followers:,.0f}")
        st.metric(label="🏅 Most Followed Artist", value=most_followed_artist)

    st.dataframe(artists_table.describe(), width=750)
    st.dataframe(artists_table.describe(include=['object']), width=750)

st.subheader("Tracks:")
tab1_tracks, tab2_tracks = st.tabs(["Data", "Descriptive Statistics"])
with tab1_tracks:
    st.dataframe(tracks_table, width=1200, height=210, hide_index=True)
with tab2_tracks:
    col1, col2 = st.columns(2)

    with col1:
        avg_popularity_track = tracks_table['Popularity'].mean()
        max_popularity_track = tracks_table['Popularity'].max()
        most_popular_track = tracks_table.loc[
            tracks_table['Popularity'].idxmax(), 'Track Name']
        max_popularity = tracks_table['Popularity'].max()

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

    st.dataframe(tracks_table.describe(), width=750)
    st.dataframe(tracks_table.describe(include=['object']), width=750)
