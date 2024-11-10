import streamlit as st
import pandas as pd
import yaml
import os


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

st.sidebar.image("images/Spotify_Full_Logo_RGB_Green.png")

st.sidebar.title("Navigation")
menu_options = ["Home", "Playlists Analysis", "Tracks Analysis", "Artists Analysis", "Albums Analysis", "Recommendations"]

choice = st.sidebar.radio("Go to", menu_options)

if choice == "Home":
    st.title("Welcome to the Spotify Data Analysis App")
    st.subheader("Subheader")
    st.write("""
    This application provides interactive visualizations and analyses of Spotify data, 
    including track popularity, audio features, artist genres, and more.
    Use the navigation menu to explore different sections.
    """)
    st.markdown("Select a section from the navigation panel to continue.")

elif choice == "Playlists Analysis":
    st.title("Playlists Analysis")

elif choice == "Tracks Analysis":
    st.title("Tracks Analysis")

elif choice == "Artists Analysis":
    st.title("Artists Analysis")

elif choice == "Albums Analysis":
    st.title("Albums Analysis")

elif choice == "Recommendations":
    st.title("Recommendations")
