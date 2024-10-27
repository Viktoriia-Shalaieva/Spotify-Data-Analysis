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

with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# pprint(config)

playlists = config['playlists']

file_path_playlists = './data/raw/playlists/'
playlist_data = spotify.get_save_playlist(token, playlists, file_path_playlists)

playlists_ids = list(playlists.values())
playlists = data_prep.create_all_playlists_table(token, playlists_ids)
print(playlists)

file_path_all_playlists = './data/preprocessed/playlists.csv'
playlists.to_csv(file_path_all_playlists, index=False, sep="~")

track_ids = playlists['track_id'].tolist()

tracks = data_prep.create_tracks_table(token, track_ids)
print(tracks)

file_path_tracks = './data/preprocessed/tracks.csv'
tracks.to_csv(file_path_tracks, index=False, sep="~")
