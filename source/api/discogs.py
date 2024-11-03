import requests


def get_genre(discogs_api_token, track_title, artist_name):
    genres = None
    url = 'https://api.discogs.com/database/search'
    params = {
        'track': track_title,
        'artist': artist_name,
        'token': discogs_api_token
    }
    try:
        response = requests.get(url, params=params)
        track = response.json()
        genres = set()
        for result in track['results']:
            if 'genre' in result:
                genres.update(result['genre'])
                print("Genre information retrieved successfully")
    except Exception as error_message:
        print(f"The following error occurred: {error_message}")

    # Return a list instead of a set for compatibility with DataFrame and file storage
    return list(genres)


def get_genre_artist(discogs_api_token, artist_name):
    genres = None
    url = 'https://api.discogs.com/database/search'
    params = {
        'artist': artist_name,
        'token': discogs_api_token,
    }
    try:
        response = requests.get(url, params=params)
        track = response.json()
        genres = set()
        for result in track['results']:
            if 'genre' in result:
                genres.update(result['genre'])
                print("Genre information retrieved successfully")
    except Exception as error_message:
        print(f"The following error occurred: {error_message}")

    # Return a list instead of a set for compatibility with DataFrame and file storage
    return list(genres)
