from pprint import pprint
import pandas as pd
from source.api import spotify
from source.preprocessing import data_prep
import yaml
from logs.logger_config import logger
import os


pd.set_option('display.max_columns', None)

spotify_api_token = spotify.get_spotify_access_token()
logger.info(f"Spotify API token: {spotify_api_token}")

discogs_api_token = 'EaALIPVnUVkCSfqeUhhWzcdXZfgXNvERIHfabBFh'
logger.info(f"Discogs API token: {discogs_api_token}")

with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

playlists_all = config['playlists']

with open('config/path_config.yaml', 'r') as config_file:
    path_config = yaml.safe_load(config_file)
#
data_dir = path_config['data_dir'][0]
raw_dir = path_config['raw_dir'][0]
file_paths = {file_name: os.path.join(data_dir, file_name) for file_name in path_config['files_names']}

playlists_path = str(file_paths['playlists.csv'])
albums_path = str(file_paths['albums.csv'])
artists_path = str(file_paths['artists.csv'])
artists_genres_discogs_path = str(file_paths['artists_genres_discogs.csv'])
artists_genres_full_path = str(file_paths['artists_genres_full.csv'])
artists_genres_full_unknown_path = str(file_paths['artists_genres_full_unknown.csv'])
tracks_path = str(file_paths['tracks.csv'])
tracks_audio_features_path = str(file_paths['tracks_audio_features.csv'])
tracks_genres_discogs_path = str(file_paths['tracks_genres_discogs.csv'])

# playlist_data = spotify.get_save_playlist(spotify_api_token, playlists_all, raw_dir)
#
# playlists_ids = list(playlists_all.values())
# playlists = data_prep.create_all_playlists_table(spotify_api_token, playlists_ids)
# logger.debug(playlists)
#
# playlists.to_csv(playlists_path, index=False, sep="~")
# logger.info(f"Playlists data saved to {playlists_path}")

playlists_table = pd.read_csv(playlists_path, sep="~")

# album_ids = set(playlists_table['album_id'])
# artist_ids = set(playlists_table['artist_id'])
# track_ids = set(playlists_table['track_id'])

# albums = data_prep.create_albums_table(spotify_api_token, album_ids)
# logger.debug(albums)
#
# albums.to_csv(albums_path, index=False, sep="~")
# logger.info(f"Albums data saved to {albums_path}")
#
# artists = data_prep.create_artists_table(spotify_api_token, artist_ids)
# logger.debug(artists)
#
# artists.to_csv(artists_path, index=False, sep="~")
# logger.info(f"Artists data saved to {artists_path}")
# #
# tracks = data_prep.create_tracks_table(spotify_api_token, track_ids)
# logger.debug(tracks)
#
# tracks.to_csv(tracks_path, index=False, sep="~")
# logger.info(f"Tracks data saved to {tracks_path}")
#
# tracks_audio_features = data_prep.create_tracks_af_table(spotify_api_token, track_ids)
# logger.debug(tracks_audio_features)
#
# tracks_audio_features.to_csv(tracks_audio_features_path, index=False, sep="~")
# logger.info(f"Track audio features saved to {tracks_audio_features_path}")
# #
# tracks_genres_discogs = data_prep.create_track_genre_table(playlists_table, discogs_api_token)
# logger.debug(tracks_genres_discogs)
#
# tracks_genres_discogs.to_csv(tracks_genres_discogs_path, index=False, sep="~")
# logger.info(f"Track genres saved to {tracks_genres_discogs_path}")
#
tracks_genres_discogs = pd.read_csv(tracks_genres_discogs_path, sep="~")
#
# empty_tracks_genres_discogs = (tracks_genres_discogs['track_genre'] == '[]').sum()
# logger.info(f"Number of empty track genres in tracks_genres.csv: {empty_tracks_genres_discogs}")
#
artists = pd.read_csv(artists_path, sep="~")
# logger.debug(artists)
# #
# empty_genre_count_art = (artists['artist_genres'] == '[]').sum()
# logger.info(f"Number of empty artist genres in artists.csv: {empty_genre_count_art}")
#
# artists_genres_discogs = data_prep.create_artist_genre_table(artists, discogs_api_token)
# logger.debug(artists_genres_discogs)
#
# artists_genres_discogs.to_csv(artists_genres_discogs_path, index=False, sep="~")
#
artists_genres_discogs = pd.read_csv(artists_genres_discogs_path, sep="~")
#
# empty_artists_genres_count = (artists_genres_discogs['artist_genre'] == '[]').sum()
# logger.info(f"Number of empty genres in artists_genres_discogs.csv: {empty_artists_genres_count}")
#
artists['artist_genres'] = artists['artist_genres'].replace('[]', pd.NA)

artists = artists.merge(artists_genres_discogs, on='artist_name', how='left')
logger.debug(artists)
artists['artist_genres'] = artists['artist_genres'].fillna(artists['artist_genre'])
artists = artists.drop(columns=['artist_genre'])
artists.to_csv(artists_genres_full_path, index=False, sep="~")

artists['artist_genres'] = artists['artist_genres'].replace('[]', 'unknown genre')

artists.to_csv(artists_genres_full_unknown_path, index=False, sep="~")
logger.debug(artists)
#
artists_genres_full_unknown = pd.read_csv(artists_genres_full_unknown_path, sep="~")
empty_genre_count_art = (artists_genres_full_unknown['artist_genres'] == 'unknown genre').sum()
logger.info(f"Number of empty artist genres in artists_genre_full.csv: {empty_genre_count_art}")

albums_table = pd.read_csv(albums_path, sep='~')
artists_genres_full = pd.read_csv(artists_genres_full_path, sep='~')
tracks_table = pd.read_csv(tracks_path, sep='~')
tracks_audio_features_table = pd.read_csv(tracks_audio_features_path, sep='~')
tracks_genres_discogs_table = pd.read_csv(tracks_genres_discogs_path, sep='~')

logger.debug(albums_table.info())
logger.debug(artists.info())
logger.debug(artists_genres_discogs.info())
logger.debug(artists_genres_full.info())
logger.debug(artists_genres_full_unknown.info())
logger.debug(playlists_table.info())
logger.debug(tracks_table.info())
logger.debug(tracks_audio_features_table.info())
logger.debug(tracks_genres_discogs_table.info())

print('------------------ artist_genres type')
print(type(artists_genres_full['artist_genres']))

# Use the .apply() method to apply the eval function to each element in the 'artist_genres' column
# The eval function converts the string representation of lists back into actual Python lists
artists_genres_full['artist_genres'] = artists_genres_full['artist_genres'].apply(eval)

unique_genres = set()

for genres in artists_genres_full['artist_genres']:
    unique_genres.update(genres)

unique_genres_list = sorted(unique_genres)
pprint(unique_genres_list)
num_unique_genres = len(unique_genres_list)
print(num_unique_genres)
