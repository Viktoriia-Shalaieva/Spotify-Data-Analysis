import requests


def get_track(discogs_api_token, track_title, artist_name, album):
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
