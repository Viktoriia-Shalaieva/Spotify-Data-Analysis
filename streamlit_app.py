import streamlit as st
import pandas as pd
import yaml
import os
import plotly.express as px


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

st.sidebar.image("images/songs.png")

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
    st.write("Analyze various Spotify playlists data.")
    playlist_names = playlists_table['playlist_name'].unique()
    total_playlists = playlists_table['playlist_id'].nunique()
    average_followers = playlists_table['playlist_followers_total'].mean()
    total_unique_tracks = playlists_table['track_id'].nunique()
    min_followers = playlists_table['playlist_followers_total'].min()
    max_followers = playlists_table['playlist_followers_total'].max()

    max_followers_playlist = playlists_table.sort_values(by='playlist_followers_total', ascending=False).iloc[0]
    min_followers_playlist = playlists_table.sort_values(by='playlist_followers_total').iloc[0]

    st.subheader("Playlists Analysis - Overview Statistics")

    st.metric(label="Total Number of Playlists", value=total_playlists)
    st.metric(label="Average Number of Followers per Playlist", value=f"{average_followers:.0f}")
    st.metric(label="Total Number of Unique Tracks", value=total_unique_tracks)

    st.subheader("Playlist with Maximum Followers")
    st.write(f"Playlist Name: {max_followers_playlist['playlist_name']}")
    st.write(f"Number of Followers: {max_followers_playlist['playlist_followers_total']}")

    st.subheader("Playlist with Minimum Followers")
    st.write(f"Playlist Name: {min_followers_playlist['playlist_name']}")
    st.write(f"Number of Followers: {min_followers_playlist['playlist_followers_total']}")

    followers_data = playlists_table[['playlist_name', 'playlist_followers_total']].drop_duplicates()
    followers_data.columns = ['Playlist Name', 'Number of Followers']

    followers_data = followers_data.sort_values(by='Number of Followers', ascending=False)

    fig_followers = px.bar(followers_data,
                           x='Playlist Name',
                           y='Number of Followers',
                           color="Playlist Name",
                           title='Number of Followers per Playlist')
    st.plotly_chart(fig_followers)

    avg_popularity = playlists_table.groupby('playlist_name')['track_popularity'].mean().reset_index()
    avg_popularity.columns = ['Playlist Name', 'Average Popularity']
    avg_popularity = avg_popularity.sort_values(by='Average Popularity', ascending=False)

    fig = px.bar(avg_popularity,
                 x='Playlist Name',
                 y='Average Popularity',
                 title='Average Track Popularity Across Playlists')

    st.plotly_chart(fig)

    selected_playlist = st.selectbox("Select a Playlist", playlist_names)
    filtered_data = playlists_table[playlists_table['playlist_name'] == selected_playlist]

    st.write(f"Data for {selected_playlist}:")
    st.dataframe(filtered_data)

    fig_track_popularity = px.histogram(filtered_data,
                                        x='track_popularity',
                                        nbins=20,
                                        title=f"Track Popularity Distribution in {selected_playlist}")
    st.plotly_chart(fig_track_popularity)

elif choice == "Tracks Analysis":
    st.title("Tracks Analysis")

elif choice == "Artists Analysis":
    st.title("Artists Analysis")

elif choice == "Albums Analysis":
    st.title("Albums Analysis")

elif choice == "Recommendations":
    st.title("Recommendations")
