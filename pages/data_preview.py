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
tracks_audio_features_path = str(file_paths['tracks_audio_features.csv'])

playlists_table = pd.read_csv(playlists_path, sep="~")
albums_table = pd.read_csv(albums_path, sep='~')
artists_genres_full_unknown = pd.read_csv(artists_genres_full_unknown_path, sep='~')
tracks_table = pd.read_csv(tracks_path, sep='~')
tracks_audio_features_table = pd.read_csv(tracks_audio_features_path, sep='~')

playlists_table['playlist_id'] = playlists_table['playlist_id'].astype(str)
albums_table['album_id'] = albums_table['album_id'].astype(str)
artists_genres_full_unknown['artist_id'] = artists_genres_full_unknown['artist_id'].astype(str)
tracks_table['track_id'] = tracks_table['track_id'].astype(str)
tracks_audio_features_table['track_id'] = tracks_audio_features_table['track_id'].astype(str)

total_playlists = playlists_table['playlist_id'].nunique()
average_followers = playlists_table['playlist_followers_total'].mean()
total_unique_tracks = playlists_table['track_id'].nunique()

max_followers_playlist = playlists_table.sort_values(by='playlist_followers_total', ascending=False).iloc[0]
min_followers_playlist = playlists_table.sort_values(by='playlist_followers_total').iloc[0]

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

with st.expander("Playlists"):
    st.dataframe(playlists_table, height=210, hide_index=True)
    st.write("Descriptive Statistics for Playlists:")
    st.dataframe(playlists_table.describe(), width=1200)
    st.dataframe(playlists_table.describe(include=['object']), width=1200)

st.subheader("Playlists:")

tab1_playlists, tab2_playlists = st.tabs(["Data", "Descriptive Statistics"])

with tab1_playlists:
    st.dataframe(playlists_table, height=210,  hide_index=True)
with tab2_playlists:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        max_followers = playlists_table['playlist_followers_total'].max()
        most_followed_playlist = playlists_table.loc[
            playlists_table['playlist_followers_total'].idxmax(), 'country'
        ]
        avg_followers = playlists_table['playlist_followers_total'].mean()

        with st.container(border=True):
            st.metric(label="🏆 Most Followers", value=f"{max_followers:,.0f}")
            st.metric(label="🎶 Playlist with Most Followers", value=most_followed_playlist)

    with col2:
        total_tracks = len(playlists_table['track_id'])
        unique_tracks = playlists_table['track_id'].nunique()

        with st.container(border=True):
            st.metric(label="🎵 Total Tracks", value=total_tracks)
            st.metric(label="🎵 Unique Tracks", value=unique_tracks)

    with col3:
        total_artists = len(playlists_table['artist_id'])
        unique_artists = playlists_table['artist_id'].nunique()

        with st.container(border=True):
            st.metric(label="🎤 Total Artists", value=total_artists)
            st.metric(label="🎤 Unique Artists", value=unique_artists)

    with col4:
        total_albums = len(playlists_table['album_id'])
        unique_albums = playlists_table['album_id'].nunique()

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
        avg_popularity = albums_table['album_popularity'].mean()
        max_popularity = albums_table['album_popularity'].max()

        st.metric(label="🔥 Avg. Album Popularity", value=f"{avg_popularity:.1f}")
        st.metric(label="🎉 Max Album Popularity", value=max_popularity)

    with col2:
        avg_tracks = albums_table['album_total_tracks'].mean()
        max_tracks = albums_table['album_total_tracks'].max()

        st.metric(label="🎵 Avg. Tracks/Album", value=f"{avg_tracks:.0f}")
        st.metric(label="🎵 Max Tracks/Album", value=max_tracks)

    with col3:
        earliest_release = albums_table['album_release_date'].min()
        latest_release = albums_table['album_release_date'].max()

        st.metric(label="📅 Earliest Release", value=earliest_release)
        st.metric(label="📅 Latest Release", value=latest_release)

    st.dataframe(albums_table.describe(), width=750)
    st.dataframe(albums_table.describe(include=['object']), width=750)

st.subheader("Artists:")
tab1_artists, tab2_artists = st.tabs(["Data", "Descriptive Statistics"])
with tab1_artists:
    st.dataframe(artists_genres_full_unknown, width=1200, height=210, hide_index=True)
with tab2_artists:
    col1, col2 = st.columns(2)

    with col1:
        avg_popularity = artists_genres_full_unknown['artist_popularity'].mean()
        most_popular_artist = artists_genres_full_unknown.loc[artists_genres_full_unknown['artist_popularity'].idxmax(), 'artist_name']
        max_popularity = artists_genres_full_unknown['artist_popularity'].max()

        st.metric(label="🔥 Avg. Artist Popularity", value=f"{avg_popularity:.1f}")
        st.metric(label="🏆 Most Popular Artist", value=most_popular_artist)
        st.metric(label="🎉 Max Artist Popularity", value=max_popularity)

    with col2:
        avg_followers_artist = artists_genres_full_unknown['artist_followers'].mean()
        max_followers = artists_genres_full_unknown['artist_followers'].max()
        most_followed_artist = artists_genres_full_unknown.loc[artists_genres_full_unknown['artist_followers'].idxmax(), 'artist_name']

        st.metric(label="👥 Avg. Followers/Artist", value=f"{avg_followers_artist:,.0f}")
        st.metric(label="🌟 Max Followers", value=f"{max_followers:,.0f}")
        st.metric(label="🏅 Most Followed Artist", value=most_followed_artist)

    st.dataframe(artists_genres_full_unknown.describe(), width=750)
    st.dataframe(artists_genres_full_unknown.describe(include=['object']), width=750)

st.subheader("Tracks:")
tab1_tracks, tab2_tracks = st.tabs(["Data", "Descriptive Statistics"])
with tab1_tracks:
    st.dataframe(tracks_table, width=1200, height=210, hide_index=True)
with tab2_tracks:
    col1, col2 = st.columns(2)

    with col1:
        avg_popularity_track = tracks_table['track_popularity'].mean()
        max_popularity_track = tracks_table['track_popularity'].max()
        most_popular_track = tracks_table.loc[
            tracks_table['track_popularity'].idxmax(), 'track_name']
        max_popularity = tracks_table['track_popularity'].max()

        st.metric(label="🔥 Avg. Track Popularity", value=f"{avg_popularity_track:.1f}")
        st.metric(label="🏆 Most Popular Track", value=most_popular_track)
        st.metric(label="🎉 Max Track Popularity", value=max_popularity_track)

    with col2:
        avg_duration = (tracks_table['track_duration_ms'].mean() / 60000).round(2)
        max_duration = (tracks_table['track_duration_ms'].max() / 60000).round(2)
        min_duration = (tracks_table['track_duration_ms'].min() / 60000).round(2)

        st.metric(label="⏱️ Avg. Duration (min)", value=f"{avg_duration}")
        st.metric(label="⏳ Max Duration (min)", value=f"{avg_duration}")
        st.metric(label="⏱️ Min Duration (min)", value=f"{avg_duration}")

    st.dataframe(tracks_table.describe(), width=750)
    st.dataframe(tracks_table.describe(include=['object']), width=750)

st.subheader("Tracks Audio Features:")
tab1_tracks_af, tab2_tracks_af = st.tabs(["Data", "Descriptive Statistics"])
with tab1_tracks_af:
    st.dataframe(tracks_audio_features_table, width=1200, height=210, hide_index=True)
with tab2_tracks_af:
    st.dataframe(tracks_audio_features_table.describe(), width=750)
    st.dataframe(tracks_audio_features_table.describe(include=['object']), width=750)
#
# st.subheader("Playlists:")
# st.dataframe(playlists_table, width=750, height=210, hide_index=True)
# st.write("Descriptive Statistics for Playlists:")
# st.dataframe(playlists_table.describe())
# st.dataframe(playlists_table.describe(include=['object']))
#
# st.subheader("Albums:")
# st.dataframe(albums_table, width=750, height=210, hide_index=True)
# st.write("Descriptive Statistics for Albums:")
# st.dataframe(albums_table.describe())
# st.dataframe(albums_table.describe(include=['object']))
#
# st.subheader("Artists:")
# st.dataframe(artists_genres_full_unknown, width=750, height=210, hide_index=True)
# st.write("Descriptive Statistics for Artists:")
# st.dataframe(artists_genres_full_unknown.describe(), width=750, height=210)
# st.dataframe(artists_genres_full_unknown.describe(include=['object']), width=750)
#
# st.subheader("Tracks:")
# st.dataframe(tracks_table, width=750, height=210, hide_index=True)
# st.write("Descriptive Statistics for Tracks:")
# st.dataframe(tracks_table.describe(), width=750, height=210)
# st.dataframe(tracks_table.describe(include=['object']), width=750)
#
# st.subheader("Tracks Audio Features:")
# st.dataframe(tracks_audio_features_table, width=750, height=210, hide_index=True)
# st.write("Descriptive Statistics for Tracks Audio Features:")
# st.dataframe(tracks_audio_features_table.describe())
# st.dataframe(tracks_audio_features_table.describe(include=['object']))
