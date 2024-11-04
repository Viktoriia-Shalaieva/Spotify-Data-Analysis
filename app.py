from pprint import pprint
import pandas as pd
from source.api import spotify
from source.preprocessing import data_prep
import yaml
from logs.logger_config import logger
from source.utils import file_utils


pd.set_option('display.max_columns', None)

spotify_api_token = spotify.get_spotify_access_token()
logger.info(f"Spotify API token: {spotify_api_token}")

discogs_api_token = 'EaALIPVnUVkCSfqeUhhWzcdXZfgXNvERIHfabBFh'
logger.info(f"Discogs API token: {discogs_api_token}")

with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# pprint(config)

playlists = config['playlists']

file_path_playlists = './data/raw/playlists/'
# playlist_data = spotify.get_save_playlist(spotify_api_token, playlists, file_path_playlists)
#
# playlists_ids = list(playlists.values())
# playlists = data_prep.create_all_playlists_table(spotify_api_token, playlists_ids)
# print(playlists)

file_path_all_playlists = './data/preprocessed/playlists.csv'
# playlists.to_csv(file_path_all_playlists, index=False, sep="~")
# logger.info(f"Playlists data saved to {file_path_all_playlists}")

# playlists_table = pd.read_csv(file_path_all_playlists, sep="~")

track_ids = set(file_utils.playlists_table['track_id'])
pprint(track_ids)

# tracks = data_prep.create_tracks_table(spotify_api_token, track_ids)
# print(tracks)
#
# file_path_tracks = './data/preprocessed/tracks.csv'
# tracks.to_csv(file_path_tracks, index=False, sep="~")
# logger.info(f"Tracks data saved to {file_path_tracks}")
#
# album_ids = set(playlists_table['album_id'])
#
# albums = data_prep.create_albums_table(spotify_api_token, album_ids)
# print(albums)
#
# file_path_albums = './data/preprocessed/albums.csv'
# albums.to_csv(file_path_albums, index=False, sep="~")
# logger.info(f"Albums data saved to {file_path_albums}")
#
# tracks_audio_features = data_prep.create_tracks_af_table(spotify_api_token, track_ids)
# print(tracks_audio_features)
#
# file_path_tracks_af = './data/preprocessed/tracks_audio_features.csv'
# tracks_audio_features.to_csv(file_path_tracks_af, index=False, sep="~")
# logger.info(f"Track audio features saved to {file_path_tracks_af}")
#
# artist_ids = set(playlists_table['artist_id'])
# pprint(artist_ids)
#
# artists = data_prep.create_artists_table(spotify_api_token, artist_ids)
# print(artists)
#
file_path_artists = './data/preprocessed/artists.csv'
# artists.to_csv(file_path_artists, index=False, sep="~")
# logger.info(f"Artists data saved to {file_path_artists}")
#
# tracks_genres = data_prep.create_track_genre_table(playlists_table, discogs_api_token)
# print(tracks_genres)

# tracks_genres_path = './data/preprocessed/tracks_genres.csv'
# tracks_genres.to_csv(tracks_genres_path, index=False, sep="~")
# logger.info(f"Track genres saved to {tracks_genres_path}")
#
# tracks_genres = pd.read_csv(tracks_genres_path, sep="~")
#
# empty_genre_count_tg = (tracks_genres['track_genre'] == '[]').sum()
# # logger.info(f"Number of empty track genres in tracks_genres.csv: {empty_genre_count_tg}")
# #
# artists_path = './data/preprocessed/artists.csv'
# artists = pd.read_csv(artists_path, sep="~")
# print(artists)
#
# # empty_genre_count_art = (artists['artist_genres'] == '[]').sum()
# # logger.info(f"Number of empty artist genres in artists.csv: {empty_genre_count_art}")
# #
artists_table = pd.read_csv(file_path_artists, sep="~")
#
# artists_genres_discogs = data_prep.create_artist_genre_table(artists_table, discogs_api_token)
# print(artists_genres_discogs)
#
artists_genres_discogs_path = './data/preprocessed/artists_genres_discogs.csv'
# artists_genres_discogs.to_csv(artists_genres_path, index=False, sep="~")
# #
artists_genres_discogs = pd.read_csv(artists_genres_discogs_path, sep="~")
empty_genre_count_art = (artists_genres_discogs['artist_genre'] == '[]').sum()
logger.info(f"Number of empty genres in artists_genres_discogs.csv: {empty_genre_count_art}")

artists_table['artist_genres'] = artists_table['artist_genres'].replace('[]', pd.NA)

artists = artists_table.merge(artists_genres_discogs, on='artist_id', how='left')
print(artists)
artists['artist_genres'] = artists['artist_genres'].fillna(artists['artist_genre'])
print(artists)

artists_genre_full_path = './data/preprocessed/artists_genres_full.csv'
artists = artists.drop(columns=['artist_genre', 'artist_name_y'])
artists = artists.rename(columns={'artist_name_x': 'artist_name'})
artists.to_csv(artists_genre_full_path, index=False, sep="~")
print(artists)

artists_genre_full = pd.read_csv(artists_genre_full_path, sep="~")
empty_genre_count_art = (artists_genre_full['artist_genres'] == '[]').sum()
logger.info(f"Number of empty artist genres in artists_genre_full.csv: {empty_genre_count_art}")
