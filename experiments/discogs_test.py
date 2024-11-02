import requests
import time


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


# def get_genre(discogs_api_token, track_title, artist_name):
#     url = 'https://api.discogs.com/database/search'
#     params = {
#         'track': track_title,
#         'artist': artist_name,
#         'token': discogs_api_token
#     }
#     response = requests.get(url, params=params)
#     track = response.json()
#     genres = set()
#     # for result in track['results']:
#     #     if 'genre' in result:
#     #         for genre in result['genre']:
#     #             genres.add(genre)
#     for result in track['results']:
#         if 'genre' in result:
#             genres.update(result['genre'])
#     return list(genres)


def get_genre(discogs_api_token, track_title, artist_name):
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
        # for result in track['results']:
        #     if 'genre' in result:
        #         for genre in result['genre']:
        #             genres.add(genre)
        for result in track['results']:
            if 'genre' in result:
                genres.update(result['genre'])
                print("Genre information retrieved successfully")
    except Exception as error_message:
        print(f"The following error occurred: {error_message}")

    return list(genres)


# def get_genre(discogs_api_token, track_title, artist_name, max_retries=3):
#     url = 'https://api.discogs.com/database/search'
#     params = {
#         'track': track_title,
#         'artist': artist_name,
#         'token': discogs_api_token
#     }
#     retries = 0
#
#     while retries < max_retries:
#         response = requests.get(url, params=params)
#
#         if response.status_code == 200:
#             track_data = response.json()
#
#             if 'results' in track_data:
#                 genres = set()
#                 for result in track_data['results']:
#                     if 'genre' in result:
#                         genres.update(result['genre'])
#                 return list(genres) if genres else None
#             else:
#                 print(f"No results found for track: {track_title} by artist: {artist_name}")
#                 return None
#         elif response.status_code == 429:
#             print(f"Rate limit exceeded for {track_title} by {artist_name}. Retrying...")
#             retries += 1
#             time.sleep(2 ** retries)
#         else:
#             print(f"Failed to retrieve genre for {track_title} by {artist_name}. Status code: {response.status_code}")
#             return None
#
#     print(f"Max retries reached for {track_title} by {artist_name}. Skipping...")
#     return None
