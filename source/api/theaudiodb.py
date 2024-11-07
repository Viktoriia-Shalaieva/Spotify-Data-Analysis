import requests
from logs.logger_config import logger
from pprint import pprint


# def get_track_genre_theaudiodb(track_name, artist_name):
#     url = f"https://www.theaudiodb.com/api/v1/json/2/searchtrack.php?s={artist_name}&t={track_name}"
#     try:
#         response = requests.get(url)
#         data = response.json()
#         logger.info("Track information retrieved successfully")
#         if data['track']:
#             genre = data['track'][0].get('strGenre', 'Genre not found')
#             return genre
#         else:
#             return 'Track not found'
#
#     except Exception as error_message:
#         logger.error(f"Failed to retrieve track {track_name}: {error_message}")

#
# def get_track_genre_theaudiodb(track_title, artist_name):
#     genres = None
#     url = f"https://www.theaudiodb.com/api/v1/json/2/searchtrack.php"
#     params = {
#         's': artist_name,
#         't': track_title
#     }
#     try:
#         response = requests.get(url, params=params)
#         track_data = response.json()
#         genres = set()
#         if track_data and track_data.get('track'):
#             genre = track_data['track'][0].get('strGenre')
#             if genre:
#                 genres.add(genre)
#                 logger.info(
#                     f"Genre information retrieved successfully for track '{track_title}' by artist '{artist_name}'")
#         else:
#             logger.warning(f"Track '{track_title}' by artist '{artist_name}' not found or no genre available.")
#     except Exception as error_message:
#         logger.error(f"Failed to retrieve genre for track '{track_title}' by artist '{artist_name}': {error_message}")
#
#     # Return a list instead of a set for compatibility with DataFrame and file storage
#     return list(genres) if genres else []
#
#
# artist = "Billie Eilish"
# track = "WILDFLOWER"
# track_details = get_track_genre_theaudiodb(track, artist)
# pprint(track_details)
#
#
# def get_track_details_theaudiodb(track_name, artist_name):
#     url = f"https://www.theaudiodb.com/api/v1/json/2/searchtrack.php?s={artist_name}&t={track_name}"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             logger.info("Track information retrieved successfully")
#             return data  # Return the full JSON response
#         else:
#             logger.error(f"Failed to retrieve track {track_name}. HTTP Status Code: {response.status_code}")
#             return None
#     except Exception as error_message:
#         logger.error(f"Failed to retrieve track {track_name}: {error_message}")
#         return None
#
# # artist = "Coldplay"
# # track = "Yellow"
# # track_details = get_track_details_theaudiodb(artist, track)
# # pprint(track_details)
#
#
# print('--------------------------------------')
# artist2 = "Billie Eilish"
# track2 = "WILDFLOWER"
# track_details2 = get_track_details_theaudiodb(track2, artist2)
# pprint(track_details2)
#
#
#
# def get_track_details_theaudiodb_(track_name, artist_name):
#     url = f"https://www.theaudiodb.com/api/v1/json/2/searchtrack.php?s={artist_name}&t={track_name}"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             logger.info("Track information retrieved successfully")
#             if data['track']:
#                 for track in data['track']:
#                     if track['strTrack'].lower() == track_name.lower() and track['strArtist'].lower() == artist_name.lower():
#                         return track
#                 logger.warning(f"Exact match for track '{track_name}' by '{artist_name}' not found.")
#                 return None
#             else:
#                 logger.warning(f"Track '{track_name}' by '{artist_name}' not found.")
#                 return None
#         else:
#             logger.error(f"Failed to retrieve track '{track_name}'. HTTP Status Code: {response.status_code}")
#             return None
#     except Exception as error_message:
#         logger.error(f"Failed to retrieve track '{track_name}': {error_message}")
#         return None
#
# artist2 = "Bruno Mars"
# track2 = "Locked out of Heaven"
# track_details2 = get_track_details_theaudiodb_(track2, artist2)
# pprint(track_details2)


def get_artist_details_theaudiodb(artist_id):
    url = f"https://www.theaudiodb.com/api/v1/json/2/artist.php?i={artist_id}"
    response = requests.get(url)
    data = response.json()
    return data


artist_id = 111329
artist_details = get_artist_details_theaudiodb(artist_id)
pprint(artist_details)
