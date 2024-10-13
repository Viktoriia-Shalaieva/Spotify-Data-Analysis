import requests


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


def get_genre(access_token):
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
