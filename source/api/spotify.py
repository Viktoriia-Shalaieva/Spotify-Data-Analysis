import os
import requests
import json
from slugify import slugify
from urllib.parse import urljoin


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

    return None


def get_playlist(access_token, playlist_id):
    playlist_info = None
    # url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    url_base = "https://api.spotify.com/v1/playlists/"
    # url = os.path.join(url_base, playlist_id)
    url = urljoin(url_base, playlist_id)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        # Converts the API response (in JSON format) into a Python dictionary for further processing.
        playlist_info = response.json()
        print("Playlist information retrieved successfully")
    except Exception as error_message:
        print(f"The following error occurred: {error_message}")

    return playlist_info


def get_save_playlist(token, playlists, file_path):
    os.makedirs(file_path, exist_ok=True)
    for playlist_name, playlist_id in playlists.items():
        playlist_info = get_playlist(token, playlist_id)

        if playlist_info:
            # file_name = playlist_name.replace(' ', '_').replace('-', '').replace('__', '_').lower() + '.json'
            # file_path_playlist = file_path + file_name
            file_name = slugify(playlist_name) + '.json'
            file_path_playlist = os.path.join(file_path, file_name)

            try:
                with open(file_path_playlist, 'w') as file:
                    json.dump(playlist_info, file)
                print(f"Playlist {playlist_name} saved successfully")
            except Exception as error_message:
                print(f"Failed to save playlist {playlist_name}: {error_message}")
        else:
            print(f"Failed to retrieve playlist {playlist_name}")

    return None


def get_track(access_token, track_id):
    track_info = None
    url_base = "https://api.spotify.com/v1/tracks/"
    url = urljoin(url_base, track_id)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        # Converts the API response (in JSON format) into a Python dictionary for further processing.
        track_info = response.json()
        print("Track information retrieved successfully")
    except Exception as error_message:
        print(f"The following error occurred: {error_message}")

    return track_info


def get_album(access_token, album_id):
    album_info = None
    # url = f"https://api.spotify.com/v1/albums/{album_id}"
    url_base = "https://api.spotify.com/v1/albums/"
    url = urljoin(url_base, album_id)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        album_info = response.json()
        print("Album information retrieved successfully")
    except Exception as error_message:
        print(f"The following error occurred: {error_message}")

    return album_info


def get_track_audio_features(access_token, track_id):
    track_audio_info = None
    url_base = "https://api.spotify.com/v1/audio-features/"
    url = urljoin(url_base, track_id)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        track_audio_info = response.json()
        print("Track Audio Features information retrieved successfully")
    except Exception as error_message:
        print(f"The following error occurred: {error_message}")

    return track_audio_info


def get_artist(access_token, artist_id):
    artist_info = None
    url_base = "https://api.spotify.com/v1/artists/"
    url = urljoin(url_base, artist_id)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        artist_info = response.json()
        print("Artist information retrieved successfully")

    except Exception as error_message:
        print(f"The following error occurred: {error_message}")

    return artist_info
