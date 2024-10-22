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
