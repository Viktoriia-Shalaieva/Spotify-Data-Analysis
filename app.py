from source import api_calls
from pprint import pprint
import json
# from source.api_calls import *
# from source.api_calls import get_spotify_access_token


token = api_calls.get_spotify_access_token()
print(token)
#
# print('--------------------Marilyn Manson')
# marilyn_manson_id = '2VYQTNDsvvKN9wmU5W7xpj'
# artist_json_manson = api_calls.get_artist(marilyn_manson_id, token)
# pprint(artist_json_manson)
#
# print('--------------------track SAY10 Marilyn Manson')
# mm_say10_id = '3sxNhARfL8uj7NlMqwF61p'
# track_json_mm_say10 = api_calls.get_track(mm_say10_id, token)
# pprint(track_json_mm_say10)
#
# print('--------------------track KILL4ME Marilyn Manson')
# mm_kill4me_id = '6UIo6YbaXihIZ72MWUpcGb'
# market = 'UA'
# track_json_mm_say10 = api_calls.get_track_market(mm_kill4me_id, market, token)
# pprint(track_json_mm_say10)
#
# print('--------------------album WE ARE CHAOS Marilyn Manson')
# mm_we_are_chaos_id = '3VOlp4Dion1qjjvhmuDZvV'
# album_json_mm_we_are_chaos_id = api_calls.get_album(mm_we_are_chaos_id, token)
# pprint(album_json_mm_we_are_chaos_id)
#
# print('--------------------Available Genre Seeds')
# genre_seeds = api_calls.get_genre(token)
# pprint(genre_seeds)
#
# print('--------------------Tracks')
# more_tracks = api_calls.get_more_tracks(token)
# pprint(more_tracks)
#
# print('--------------------Tracks_MARKET')
# more_tracks_market = api_calls.get_more_tracks_market(token, 'UA')
# pprint(more_tracks_market)
#
# print('--------------------OLD Recommendations')
# old_artist_id = '2VYQTNDsvvKN9wmU5W7xpj'
# old_genre = 'rock'
# old_track = '3sxNhARfL8uj7NlMqwF61p'
# old_recommendations = api_calls.get_recommendations_old(token, old_artist_id, old_genre, old_track)
# pprint(old_recommendations)
#
# print('--------------------Recommendations')
# artist_id = '2VYQTNDsvvKN9wmU5W7xpj'
# genre = 'hard rock'
# track = '3sxNhARfL8uj7NlMqwF61p'
# recommendations = api_calls.get_recommendations(token, artist_id, genre, track)
# pprint(recommendations)
#
# print('--------------------50 ARTISTS')
# artists_50 = api_calls.get_50_artists(token)
# pprint(artists_50)

# print('--------------------TOP 50 - UKRAINE')
# pl_top_50_ua_id = '37i9dQZEVXbKkidEfWYRuD'
# playlist_top_50_ua = api_calls.get_playlist(token, pl_top_50_ua_id)
# pprint(playlist_top_50_ua)

# # Defines the path to the file where the playlist data will be saved in JSON format
# file_pl_top_50_ua = 'C:/Users/vgrec/Desktop/Spotify_Songs/Spotify-Songs-Analysis/json/pl_top_50_ua.json'
# # Opens the file for writing and saves the retrieved playlist data in JSON format
# with open(file_pl_top_50_ua, 'w') as file:
#     # Uses json.dump to write the playlist data to the specified file in JSON format
#     json.dump(playlist_top_50_ua, file)
#
# print('--------------------TOP 50 - UKRAINE Playlist Items')
# pl_items_top_50_ua_id = '37i9dQZEVXbKkidEfWYRuD'
# playlist_items_top_50_ua = api_calls.get_playlist_items(token, pl_items_top_50_ua_id)
# pprint(playlist_items_top_50_ua)

# file_pl_items_top_50_ua = 'json/pl_items_top_50_ua.json'
# with open(file_pl_items_top_50_ua, 'w') as file:
#     json.dump(playlist_items_top_50_ua, file)

# Discogs
print('--------------------Discogs')
discogs_api_token = 'EaALIPVnUVkCSfqeUhhWzcdXZfgXNvERIHfabBFh'

print('--------------------Discogs track The Emptiness Machine Linkin Park')
track_title_lp = 'The Emptiness Machine'
artist_name_lp = 'Linkin Park'
track_release_lp = api_calls.get_track_release(discogs_api_token, track_title_lp, artist_name_lp)
pprint(track_release_lp)

print('--------------------Discogs genre The Emptiness Machine Linkin Park')
genre = api_calls.get_genre(discogs_api_token, track_title_lp, artist_name_lp)
pprint(genre)

print('--------------------Discogs genre Театр Klavdia Petrivna')
track_title_kp = 'Театр'
artist_name_kp = 'Klavdia Petrivna'
genre_kp = api_calls.get_genre(discogs_api_token, track_title_kp, artist_name_kp)
pprint(genre_kp)

print('--------------------Discogs genre Барабан Artem Pivovarov')
track_title_ap_ = 'Барабан'
artist_name_ap_ = 'Artem Pivovarov'
genre_ap_ = api_calls.get_genre(discogs_api_token, track_title_ap_, artist_name_ap_)
pprint(genre_ap_)

print('--------------------Discogs genre Барабан Klavdia Petrivna')
track_title_ap = 'Барабан'
artist_name_ap = 'Klavdia Petrivna'
genre_ap = api_calls.get_genre(discogs_api_token, track_title_ap, artist_name_ap)
pprint(genre_ap)

print('--------------------Discogs genre KEEP UP Odetari')
track_title_o = 'KEEP UP'
artist_name_o = 'Odetari'
genre_o = api_calls.get_genre(discogs_api_token, track_title_o, artist_name_o)
pprint(genre_o)
