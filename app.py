import source.preprocessing.data_preprocessing
from source import api_calls
from pprint import pprint
import json
import pandas as pd

from source.api import discogs
from source.api import spotify
from source.preprocessing import data_preprocessing
import yaml

pd.set_option('display.max_columns', None)

print('--------------------Spotify API token')
token = api_calls.get_spotify_access_token()
print(token)

print('--------------------Discogs API token')
discogs_api_token = 'EaALIPVnUVkCSfqeUhhWzcdXZfgXNvERIHfabBFh'

print('--------------------Discogs track_discogs Барабан Klavdia Petrivna Artem Pivovarov + album')
track_title_ap_ = 'Барабан'
artist_name_ap_ = 'Klavdia Petrivna', 'Artem Pivovarov'
album_ap_ = 'THE BEST'
genre_ap_ = discogs.get_track(discogs_api_token, track_title_ap_, artist_name_ap_, album_ap_)
pprint(genre_ap_)

print('--------------------Discogs genre Барабан Klavdia Petrivna')
track_title_ap = 'Барабан'
artist_name_ap = 'Klavdia Petrivna'
genre_ap = discogs.get_genre(discogs_api_token, track_title_ap, artist_name_ap)
pprint(genre_ap)

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

pprint(config)

playlists_id = config['playlists_id']
playlists = data_preprocessing.create_all_playlists(token, playlists_id)
print(playlists)

file_path_playlists = './data/preprocessed/playlists.csv'
playlists.to_csv(file_path_playlists, index=False)
