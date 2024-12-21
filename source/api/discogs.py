import requests
from logs.logger_config import logger


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
                logger.info("Genre information for artist retrieved successfully")
    except Exception as error_message:
        logger.error(f"Failed to retrieve genre for artist '{artist_name}': {error_message}")

    # Return a list instead of a set for compatibility with DataFrame and file storage
    return list(genres)
