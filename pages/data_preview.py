import streamlit as st
from modules.nav import navbar
import pandas as pd
import yaml
import os
import plotly.express as px

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

st.subheader("Playlists:")
st.dataframe(playlists_table, height=210, hide_index=True)
st.write("Descriptive Statistics for Playlists:")
st.dataframe(playlists_table.describe())
st.dataframe(playlists_table.describe(include=['object']))

st.subheader("Albums:")
st.dataframe(albums_table, height=210, hide_index=True)
st.write("Descriptive Statistics for Albums:")
st.dataframe(albums_table.describe())
st.dataframe(albums_table.describe(include=['object']))

st.subheader("Artists:")
st.dataframe(artists_genres_full_unknown, height=210, hide_index=True)
st.write("Descriptive Statistics for Artists:")
st.dataframe(artists_genres_full_unknown.describe())
st.dataframe(artists_genres_full_unknown.describe(include=['object']))

st.subheader("Tracks:")
st.dataframe(tracks_table, height=210, hide_index=True)
st.write("Descriptive Statistics for Tracks:")
st.dataframe(tracks_table.describe())
st.dataframe(tracks_table.describe(include=['object']))

st.subheader("Tracks Audio Features:")
st.dataframe(tracks_audio_features_table, height=210, hide_index=True)
st.write("Descriptive Statistics for Tracks Audio Features:")
st.dataframe(tracks_audio_features_table.describe())
st.dataframe(tracks_audio_features_table.describe(include=['object']))
