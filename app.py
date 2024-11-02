from pprint import pprint
import pandas as pd
from source.api import discogs
from source.api import spotify
from source.preprocessing import data_prep
import yaml
import time
import requests

pd.set_option('display.max_columns', None)

print('--------------------Spotify API token')
token = spotify.get_spotify_access_token()
print(token)

print('--------------------Discogs API token')
discogs_api_token = 'EaALIPVnUVkCSfqeUhhWzcdXZfgXNvERIHfabBFh'

# with open('config/config.yaml', 'r') as file:
#     config = yaml.safe_load(file)
#
# # pprint(config)
#
# playlists = config['playlists']
#
# file_path_playlists = './data/raw/playlists/'
# playlist_data = spotify.get_save_playlist(token, playlists, file_path_playlists)
#
# playlists_ids = list(playlists.values())
# playlists = data_prep.create_all_playlists_table(token, playlists_ids)
# print(playlists)
# #
file_path_all_playlists = './data/preprocessed/playlists.csv'
# playlists.to_csv(file_path_all_playlists, index=False, sep="~")

playlists_table = pd.read_csv(file_path_all_playlists, sep="~")
#
# track_ids = set(playlists_table['track_id'])
# pprint(track_ids)
#
# tracks = data_prep.create_tracks_table(token, track_ids)
# print(tracks)
#
# file_path_tracks = './data/preprocessed/tracks.csv'
# tracks.to_csv(file_path_tracks, index=False, sep="~")
#
# album_ids = set(playlists_table['album_id'])
#
# albums = data_prep.create_albums_table(token, album_ids)
# print(albums)
#
# file_path_albums = './data/preprocessed/albums.csv'
# albums.to_csv(file_path_albums, index=False, sep="~")
#
# tracks_audio_features = data_prep.create_tracks_af_table(token, track_ids)
# print(tracks_audio_features)
#
# file_path_tracks_af = './data/preprocessed/tracks_audio_features.csv'
# tracks_audio_features.to_csv(file_path_tracks_af, index=False, sep="~")
#
# artist_ids = set(playlists_table['artist_id'])
# pprint(artist_ids)

# artist_chet_singh_id = '5aWkTGq5O45ES0fDFmN1Wv'
# artist_chet_singh = spotify.get_artist(token, artist_chet_singh_id)
# pprint(artist_chet_singh)

# artists = data_prep.create_artists_table(token, artist_ids)
# print(artists)
#
# file_path_artists = './data/preprocessed/artists.csv'
# artists.to_csv(file_path_artists, index=False, sep="~")

# tracks_genres = data_prep.create_track_genre_table(playlists_table, discogs_api_token)
# print(tracks_genres)
#
# file_path_tracks_genres = './data/preprocessed/tracks_genres.csv'
# tracks_genres.to_csv(file_path_tracks_genres, index=False, sep="~")

tracks_genres_path = './data/preprocessed/tracks_genres.csv'
tracks_genres = pd.read_csv(tracks_genres_path, sep="~")

empty_genre_count_tg = (tracks_genres['track_genre'] == '[]').sum()
print(f"Number of empty track genres in tracks_genres.csv: {empty_genre_count_tg}")

artists_path = './data/preprocessed/artists.csv'
artists = pd.read_csv(artists_path, sep="~")

empty_genre_count_art = (artists['artist_genres'] == '[]').sum()
print(f"Number of empty track genres in artists.csv: {empty_genre_count_art}")
