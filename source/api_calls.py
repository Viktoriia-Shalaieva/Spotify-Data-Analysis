import requests
import pandas as pd

def get_spotify_access_token():
    client_id = 'ac3eaf00cb0845a8a8a2f60c134c328e'
    client_secret = 'bc63f9adbb3a4bea8e5c7ba13b951e8e'

    token_url = "https://accounts.spotify.com/api/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    try:
        response = requests.post(
        token_url,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        token_info = response.json()
        access_token = token_info.get("access_token")
        print("Access token retrieved successfully")
        return access_token

    except Exception as error_message:
        print(f"The following error occurred: {error_message}")


def get_artist(artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        artist_info = response.json()
        print("Artist information retrieved successfully")
        return artist_info

    except Exception as error_message:
        print(f"The following error occurred: {error_message}")


def get_track(track_id, access_token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    track_info = response.json()
    return track_info


def get_track_market(track_id, market, access_token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}?market={market}"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    track_info = response.json()
    return track_info


def get_album(album_id, access_token):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    album_info = response.json()
    return album_info


def get_genre_recom(access_token):
    url = f"https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    genre_info = response.json()
    return genre_info

def get_more_tracks(access_token):
    url = "https://api.spotify.com/v1/search"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'q': 'genre:rock',
        'type': 'track',
        'limit': 1,
    }

    response = requests.get(url, headers=headers, params=params)
    more_tracks = response.json()
    return more_tracks


def get_more_tracks_market(access_token, market):
    url = "https://api.spotify.com/v1/search"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'q': 'genre:rock',
        'type': 'track',
        'limit': 5,
        'market': market,
    }

    response = requests.get(url, headers=headers, params=params)
    more_tracks_market = response.json()
    return more_tracks_market


def get_recommendations_old(access_token, artist_id, genre, track):
    url = f"https://api.spotify.com/v1/recommendations?seed_artists={artist_id}&seed_genres={genre}&seed_tracks={track}"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'type': 'track',
        'limit': 1,
    }

    response = requests.get(url, headers=headers, params=params)
    recommendations = response.json()
    return recommendations

def get_recommendations(access_token, artist_id, genre, track):
    url = "https://api.spotify.com/v1/recommendations"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'seed_artists': artist_id,
        'seed_genres': genre,
        'seed_tracks': track,
        'limit': 1,
    }

    response = requests.get(url, headers=headers, params=params)
    recommendations = response.json()
    return recommendations


def get_50_artists(access_token):
    url = "https://api.spotify.com/v1/search"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'q': 'genre:rock',
        'type': 'artist',
        'limit': 50,
    }

    response = requests.get(url, headers=headers, params=params)
    artists = response.json()
    return artists

def get_playlist(access_token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        # Converts the API response (in JSON format) into a Python dictionary for further processing.
        playlist_info = response.json()
        print("Playlist information retrieved successfully")
        return playlist_info

    except Exception as error_message:
        print(f"The following error occurred: {error_message}")

def get_playlist_items(access_token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        playlist_items_info = response.json()
        print("Playlist items information retrieved successfully")
        return playlist_items_info

    except Exception as error_message:
        print(f"The following error occurred: {error_message}")


def get_track_discogs(discogs_api_token, track_title, artist_name):
    url = 'https://api.discogs.com/database/search'
    params = {
        'track': track_title,
        'artist': artist_name,
        'token': discogs_api_token
    }
    response = requests.get(url, params=params)
    track_release = response.json()
    return track_release


def get_track_discogs_album(discogs_api_token, track_title, artist_name, album):
    url = 'https://api.discogs.com/database/search'
    params = {
        'track': track_title,
        'artist': artist_name,
        'token': discogs_api_token,
        'album': album
    }
    response = requests.get(url, params=params)
    track_release = response.json()
    return track_release


def get_genre(discogs_api_token, track_title, artist_name):
    url = 'https://api.discogs.com/database/search'
    params = {
        'track': track_title,
        'artist': artist_name,
        'token': discogs_api_token
    }
    response = requests.get(url, params=params)
    track = response.json()
    genres = set()
    # for result in track['results']:
    #     if 'genre' in result:
    #         for genre in result['genre']:
    #             genres.add(genre)
    for result in track['results']:
        if 'genre' in result:
            genres.update(result['genre'])
    return list(genres)


def get_track_discogs(discogs_api_token, track_title, artist_name):
    url = 'https://api.discogs.com/database/search'
    params = {
        'track': track_title,
        'artist': artist_name,
        'token': discogs_api_token
    }
    response = requests.get(url, params=params)
    track = response.json()
    return track


def get_track_discogs_isrc(discogs_api_token, isrc):
    url = 'https://api.discogs.com/database/search'
    params = {
        'query': isrc,
        'token': discogs_api_token
    }
    response = requests.get(url, params=params)
    track = response.json()
    return track


# Function to normalize a JSON object by flattening nested dictionaries
# def normalize_json(data: dict) -> dict:
#     # Create an empty dictionary to store the flattened data
#     new_data = dict()
#
#     # Loop through each key-value pair in the input dictionary
#     for key, value in data.items():
#         # Check if the value is NOT a dictionary (i.e., it's already a simple value)
#         if not isinstance(value, dict):
#             # If the value is simple (not a dictionary), directly add it to the new_data dictionary
#             new_data[key] = value
#         else:
#             # If the value is a dictionary (i.e., a nested structure),
#             # loop through its key-value pairs to flatten it
#             for k, v in value.items():
#                 # Combine the original key and the nested key using an underscore as a separator
#                 # Add the flattened key-value pair to new_data
#                 new_data[key + "_" + k] = v
#
#     # Return the flattened dictionary
#     return new_data


# def normalize_json(data: dict, parent_key: str = '') -> dict:
#     new_data = dict()
#     for key, value in data.items():
#         new_key = f'{parent_key}_{key}' if parent_key else key
#         if isinstance(value, dict):
#             new_data.update(normalize_json(value, new_key))
#         elif isinstance(value, list):
#             for i, item in enumerate(value):
#                 if isinstance(item, dict):
#                     new_data.update(normalize_json(item, f'{new_key}_{i}'))
#                 else:
#                     new_data[f'{new_key}_{i}'] = item
#         else:
#             new_data[new_key] = value
#     return new_data

def create_playlist_table(playlist):
    playlist_id = playlist['id']
    playlist_name = playlist['name']
    playlist_followers_total = playlist['followers']['total']
    rows = []

    for item in playlist['tracks']['items']:
        track = item['track']
        track_added_at = item['added_at']


        row = {
            'playlist_id': playlist_id,
            'playlist_name': playlist_name,
            'playlist_followers_total': playlist_followers_total,
            'track_id': track['id'],
            'track_name': track['name'],
            'track_added_at': track_added_at,
            'track_duration_ms': track['duration_ms'],
            'track_popularity': track['popularity'],
            'track_explicit': track['explicit'],
            'track_restrictions': track.get('restrictions', {}).get('reason'),
            'track_isrc': track['external_ids'].get('isrc'),
            'track_ean': track['external_ids'].get('ids'),
            'track_upc': track['external_ids'].get('upc'),
        }

        album = track['album']

        album_info = {
            'album_id': album['id'],
            'album_name': album['name'],
            'album_release_date': album['release_date'],
            'album_type': album['album_type'],
            'album_total_tracks': album['total_tracks'],
            'album_restrictions': album.get('restrictions', {}).get('reason'),
        }

        artists_info = {
            'artist_id': ', '.join([artist['id'] for artist in track['artists']]),
            'artist_name': ', '.join([artist['name'] for artist in track['artists']]),
        }

        row.update(album_info)
        row.update(artists_info)

        rows.append(row)
    df = pd.DataFrame(rows)
    return df


def create_playlist_table_2(playlist):
    playlist_id = playlist['id']
    playlist_name = playlist['name']
    playlist_followers_total = playlist['followers']['total']
    rows = []

    for item in playlist['tracks']['items']:
        track = item['track']
        track_added_at = item['added_at']

        row = {
            'playlist_id': playlist_id,
            'playlist_name': playlist_name,
            'playlist_followers_total': playlist_followers_total,
            'album_id': track['album']['id'],
            'album_name': track['album']['name'],
            'album_release_date': track['album']['release_date'],
            'album_type': track['album']['album_type'],
            'album_total_tracks': track['album']['total_tracks'],
            'album_restrictions': track['album'].get('restrictions', {}).get('reason'),
            'artist_id': ', '.join([artist['id'] for artist in track['artists']]),
            'artist_name': ', '.join([artist['name'] for artist in track['artists']]),
            'track_id': track['id'],
            'track_name': track['name'],
            'track_added_at': track_added_at,
            'track_duration_ms': track['duration_ms'],
            'track_popularity': track['popularity'],
            'track_explicit': track['explicit'],
            'track_restrictions': track.get('restrictions', {}).get('reason'),
            'track_isrc': track['external_ids'].get('isrc'),
            'track_ean': track['external_ids'].get('ids'),
            'track_upc': track['external_ids'].get('upc'),
        }

        rows.append(row)

    df = pd.DataFrame(rows)
    return df


def create_all_playlist_df(token, playlist_ids):
    all_playlists = []
    for playlist_id in playlist_ids:
        playlist_data = get_playlist(token, playlist_id)
        df_playlist = create_playlist_table(playlist_data)
        all_playlists.append(df_playlist)

    playlists_df = pd.concat(all_playlists, ignore_index=True)
    return playlists_df
