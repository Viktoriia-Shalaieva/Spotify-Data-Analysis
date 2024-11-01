from pprint import pprint
import pandas as pd
from source.api import discogs
from source.api import spotify
from source.preprocessing import data_prep
import yaml

pd.set_option('display.max_columns', None)

print('--------------------Spotify API token')
token = spotify.get_spotify_access_token()
print(token)

print('--------------------Discogs API token')
discogs_api_token = 'EaALIPVnUVkCSfqeUhhWzcdXZfgXNvERIHfabBFh'

print('--------------------Discogs AudD token')
audd_api_token = '32f003350629bc0ef36103d8ab84ced4'

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
#
file_path_all_playlists = './data/preprocessed/playlists.csv'
# playlists.to_csv(file_path_all_playlists, index=False, sep="~")
#
# track_ids = playlists['track_id'].tolist()
#
# tracks = data_prep.create_tracks_table(token, track_ids)
# print(tracks)
#
# file_path_tracks = './data/preprocessed/tracks.csv'
# tracks.to_csv(file_path_tracks, index=False, sep="~")

playlists_table = pd.read_csv(file_path_all_playlists, sep="~")

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

# artist_ids = set(playlists_table['artist_id'])
# pprint(artist_ids)
#
# artists = data_prep.create_artists_table(token, artist_ids)
# print(artists)
#
# file_path_artists = './data/preprocessed/artists.csv'
# artists.to_csv(file_path_artists, index=False, sep="~")
