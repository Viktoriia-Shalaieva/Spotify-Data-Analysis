import streamlit as st
from modules.nav import navbar
import pandas as pd
import yaml
import os


st.set_page_config(
    page_title="Spotify Data Analysis",
    page_icon="🎵")

st.sidebar.image("images/music.png", width=150)

navbar()
st.sidebar.divider()
st.sidebar.markdown("# **Data Preview** 🧮 ")

st.title("Data Preview 🧮 ")
st.divider()

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

st.metric(label="Total Number of Playlists", value=total_playlists)
st.metric(label="Average Number of Followers per Playlist", value=f"{average_followers:.0f}")
st.metric(label="Total Number of Unique Tracks", value=total_unique_tracks)


with st.expander("Playlists"):
    st.dataframe(playlists_table, width=750, height=210, hide_index=True)
    st.write("Descriptive Statistics for Playlists:")
    st.dataframe(playlists_table.describe(), width=750)
    st.dataframe(playlists_table.describe(include=['object']), width=750)

st.subheader("Playlists:")

tab1_playlists, tab2_playlists = st.tabs(["Data", "Descriptive Statistics"])

with tab1_playlists:
    st.dataframe(playlists_table, width=750, height=210, hide_index=True)
with tab2_playlists:
    st.dataframe(playlists_table.describe(), width=750)
    st.dataframe(playlists_table.describe(include=['object']), width=750)

st.subheader("Albums:")
tab1_albums, tab2_albums = st.tabs(["Data", "Descriptive Statistics"])
with tab1_albums:
    st.dataframe(albums_table, width=750, height=210, hide_index=True)
with tab2_albums:
    st.dataframe(albums_table.describe(), width=750)
    st.dataframe(albums_table.describe(include=['object']), width=750)

st.subheader("Artists:")
tab1_artists, tab2_artists = st.tabs(["Data", "Descriptive Statistics"])
with tab1_artists:
    st.dataframe(artists_genres_full_unknown, width=750, height=210, hide_index=True)
with tab2_artists:
    st.dataframe(artists_genres_full_unknown.describe(), width=750)
    st.dataframe(artists_genres_full_unknown.describe(include=['object']), width=750)

st.subheader("Tracks:")
tab1_tracks, tab2_tracks = st.tabs(["Data", "Descriptive Statistics"])
with tab1_tracks:
    st.dataframe(tracks_table, width=750, height=210, hide_index=True)
with tab2_tracks:
    st.dataframe(tracks_table.describe(), width=750)
    st.dataframe(tracks_table.describe(include=['object']), width=750)

st.subheader("Tracks Audio Features:")
tab1_tracks_af, tab2_tracks_af = st.tabs(["Data", "Descriptive Statistics"])
with tab1_tracks_af:
    st.dataframe(tracks_audio_features_table, width=750, height=210, hide_index=True)
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
