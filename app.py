from pprint import pprint
import pandas as pd
from source.api import discogs
from source.api import spotify
from source.preprocessing import data_prep
import yaml
import json

pd.set_option('display.max_columns', None)

print('--------------------Spotify API token')
token = spotify.get_spotify_access_token()
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

# pprint(config)

playlists = config['playlists']

file_path_playlists = './data/raw/playlists/'

for playlist in playlists:
    playlist_id = playlist['id']
    playlist_name = playlist['name']

    playlist_data = spotify.get_playlist(token, playlist_id)

    file_name = playlist_name.replace(' ', '_').replace('-', '').replace('__', '_').lower() + '.json'
    print(file_name)
    file_path_playlist = file_path_playlists + file_name
    print(file_path_playlist)

    with open(file_path_playlist, 'w') as file:
        # Uses json.dump to write the playlist data to the specified file in JSON format
        json.dump(playlist_data, file)


playlists_ids = [playlist['id'] for playlist in playlists]
playlists = data_prep.create_all_playlists(token, playlists_ids)
print(playlists)

file_path_all_playlists = './data/preprocessed/playlists.csv'
playlists.to_csv(file_path_all_playlists, index=False, sep="~")
