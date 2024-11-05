import requests
from pprint import pprint

isrc = "USUM72409273"

# url = f"https://musicbrainz.org/ws/2/recording?query=isrc:{isrc}&fmt=json"
#
# response = requests.get(url, headers={"User-Agent": "YourAppName/1.0 (your.email@example.com)"})
#
# data = response.json()
# pprint(data)

# url = 'https://musicbrainz.org/ws/2/artist/2b0c41f2-7d9c-4b5a-8a2a-2b0c41f2f7d9?inc=genres'
# response = requests.get(url, headers={"User-Agent": "YourAppName/1.0 (your.email@example.com)"})
# data = response.json()
# pprint(data)
#
# isrc = "USAT21203287"
# isrc_2 = 'USWB12403466'
#
#
# def get_recording_by_isrc(isrc):
#     url = f"https://musicbrainz.org/ws/2/recording"
#     params = {
#         'query': f'isrc:{isrc}',
#         'fmt': 'json'
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     return data
#
#
# track = get_recording_by_isrc(isrc)
# pprint(track)
#
# # track_2 = get_recording_by_isrc(isrc_2)
# # pprint(track_2)


def get_artist_genres(artist_name):
    search_url = f"https://musicbrainz.org/ws/2/artist/?query=artist:{artist_name}&fmt=json"
    response = requests.get(search_url)
    data = response.json()
    pprint(data)

    if 'artists' not in data or len(data['artists']) == 0:
        print("Artist not found.")
        return None

    artist_id = data['artists'][0]['id']

    details_url = f"https://musicbrainz.org/ws/2/artist/{artist_id}?inc=tags&fmt=json"
    response = requests.get(details_url)
    artist_data = response.json()

    genres = [tag['name'] for tag in artist_data.get('tags', [])]
    return genres


artist_name = "Adele"
genres = get_artist_genres(artist_name)
print(f"Genres for {artist_name}: {genres}")
