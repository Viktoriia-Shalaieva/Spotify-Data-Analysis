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

    response = requests.post(
        token_url,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    token_info = response.json()
    access_token = token_info.get("access_token")

    return access_token


def get_artist(artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    # Check the status code
    if response.status_code == 200:
        artist_info = response.json()
        print("Artist information retrieved successfully:")
        return artist_info
    else:
        # If not successful, print the status code and error message
        print(f"Error: Received status code {response.status_code}")
        try:
            error_info = response.json()
            print("Error details:", error_info)
        # If the response doesn't contain valid JSON
        except ValueError:
            print("No JSON response received.")
        return None


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
