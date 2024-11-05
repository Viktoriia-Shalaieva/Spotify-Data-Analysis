import requests
from pprint import pprint


def get_artist_genre(artist_id):
    artist_url = f"https://api.deezer.com/artist/{artist_id}"
    artist_response = requests.get(artist_url)
    artist_data = artist_response.json()
    return artist_data


art = get_artist_genre(125)
pprint(art)
