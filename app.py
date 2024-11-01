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

# track_title = 'Театр'
# artist_name = 'Klavdia Petrivna'
# genre = discogs.get_genre(discogs_api_token, track_title, artist_name)
# pprint(genre)

print('------------------Billie Eilish WILDFLOWER genre')
track_title = 'WILDFLOWER'
artist_name = 'Billie Eilish'
genre = discogs.get_genre(discogs_api_token, track_title, artist_name)
pprint(genre)
#
# playlists_ = pd.read_csv(file_path_all_playlists, sep="~")
# for _, row in playlists_.iterrows():
#     print('----------------------------- track')
#     track_name = row['track_name']
#     print(track_name)
#     print('----------------------------- artist')
#     artists_ = row['artist_name']
#     print(artists_)
#     print('----------------------------- genre')
#     genres_ = discogs.get_genre(token, track_name, artists_)
#     print(genres_)

# def create_track_genre_table(file_path_all_playlists_, discogs_api_token_):
#     playlists_ = pd.read_csv(file_path_all_playlists_, sep="~")
#
#     rows = []
#
#     for _, row in playlists_.iterrows():
#         track_name = row['track_name']
#         artists_ = row['artist_name']
#
#         genres_ = discogs.get_genre(discogs_api_token_, track_name, artists_)
#         time.sleep(1)
#         track_genre = ", ".join(genres_) if genres_ else None
#
#         rows.append({
#                 'track_name': track_name,
#                 'artist_name': artists_,
#                 'track_genre': track_genre
#         })
#     track_genre_df = pd.DataFrame(rows, columns=['track_name', 'artist_name', 'track_genre'])
#     return track_genre_df
#
#
# genres = create_track_genre_table(file_path_all_playlists, discogs_api_token)
# print(genres)
