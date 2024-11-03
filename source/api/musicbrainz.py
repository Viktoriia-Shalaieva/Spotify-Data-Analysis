import requests
from pprint import pprint

# isrc = "USUM72409273"
#
# url = f"https://musicbrainz.org/ws/2/recording?query=isrc:{isrc}&fmt=json"
#
# response = requests.get(url, headers={"User-Agent": "YourAppName/1.0 (your.email@example.com)"})
#
# data = response.json()
# pprint(data)

isrc = "USAT21203287"
isrc_2 = 'USWB12403466'


def get_recording_by_isrc(isrc):
    url = f"https://musicbrainz.org/ws/2/recording"
    params = {
        'query': f'isrc:{isrc}',
        'fmt': 'json'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


track = get_recording_by_isrc(isrc)
pprint(track)

# track_2 = get_recording_by_isrc(isrc_2)
# pprint(track_2)
