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


def get_artist(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {
    "Authorization": f"Bearer BQCQZMJxrkf8fe8p7CDzAQaZdfRfHU0FSoV5FqzMrcZ6EuZmFN5lQqkF7M1cwa6dyOGT1FhhcxhX61OkFztnCOua6Vpf-3oNw42ziKrmNC90Il5SYbo"
    }

    response = requests.get(url, headers=headers)
    artist_info = response.json()
    return artist_info