import requests

from logs.logger_config import logger


def get_genre_artist(discogs_api_token, artist_name):
    """Retrieve a list of unique music genres associated with a given artist from the Discogs API."""
    genres = None
    url = "https://api.discogs.com/database/search"
    params = {
        "artist": artist_name,
        "token": discogs_api_token,
    }
    try:
        response = requests.get(url, params=params)
        info = response.json()
        genres = set()
        for result in info["results"]:
            if "genre" in result:
                genres.update(result["genre"])
                logger.info(f"Genre information for artist '{artist_name}' retrieved successfully")
    except Exception as error_message:
        logger.error(f"Failed to retrieve genre for artist '{artist_name}': {error_message}")

    # Return a list instead of a set for compatibility with DataFrame and file storage
    return list(genres)
