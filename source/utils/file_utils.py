import os
import pandas as pd

data_dir = './data/preprocessed'

albums_path = os.path.join(data_dir, 'albums.csv')
artists_path = os.path.join(data_dir, 'artists.csv')
artists_genres_discogs_path = os.path.join(data_dir, 'artists_genres_discogs.csv')
artists_genres_full_path = os.path.join(data_dir, 'artists_genres_full.csv')
playlists_path = os.path.join(data_dir, 'playlists.csv')
tracks_path = os.path.join(data_dir, 'tracks.csv')
tracks_audio_features_path = os.path.join(data_dir, 'tracks_audio_features.csv')
tracks_genres_path = os.path.join(data_dir, 'tracks_genres.csv')

albums_table = pd.read_csv(albums_path, sep="~")
artists_table = pd.read_csv(artists_path, sep="~")
artists_genres_discogs_table = pd.read_csv(artists_genres_discogs_path, sep="~")
artists_genres_full_table = pd.read_csv(artists_genres_full_path, sep="~")
playlists_table = pd.read_csv(playlists_path, sep="~")
tracks_table = pd.read_csv(tracks_path, sep="~")
tracks_audio_features_table = pd.read_csv(tracks_audio_features_path, sep="~")
tracks_genres_table = pd.read_csv(tracks_genres_path, sep="~")
