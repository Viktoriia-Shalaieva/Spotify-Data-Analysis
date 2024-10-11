from source import api_calls
from pprint import pprint
# from source.api_calls import *
# from source.api_calls import get_spotify_access_token


token = api_calls.get_spotify_access_token()
print(token)

print('--------------------Marilyn Manson')
marilyn_manson_id = '2VYQTNDsvvKN9wmU5W7xpj'
artist_json_manson = api_calls.get_artist(marilyn_manson_id, token)
pprint(artist_json_manson)

print('--------------------track SAY10 Marilyn Manson')
mm_say10_id = '3sxNhARfL8uj7NlMqwF61p'
track_json_mm_say10 = api_calls.get_track(mm_say10_id, token)
pprint(track_json_mm_say10)

print('--------------------track KILL4ME Marilyn Manson')
mm_kill4me_id = '6UIo6YbaXihIZ72MWUpcGb'
market = 'UA'
track_json_mm_say10 = api_calls.get_track_market(mm_kill4me_id, market, token)
pprint(track_json_mm_say10)

print('--------------------album WE ARE CHAOS Marilyn Manson')
mm_we_are_chaos_id = '3VOlp4Dion1qjjvhmuDZvV'
album_json_mm_we_are_chaos_id = api_calls.get_album(mm_we_are_chaos_id, token)
pprint(album_json_mm_we_are_chaos_id)

print('--------------------Available Genre Seeds')
genre_seeds = api_calls.get_genre(token)
pprint(genre_seeds)

print('--------------------Tracks')
more_tracks = api_calls.get_more_tracks(token)
pprint(more_tracks)

print('--------------------Tracks_MARKET')
more_tracks_market = api_calls.get_more_tracks_market(token, 'UA')
pprint(more_tracks_market)

print('--------------------OLD Recommendations')
old_artist_id = '2VYQTNDsvvKN9wmU5W7xpj'
old_genre = 'rock'
old_track = '3sxNhARfL8uj7NlMqwF61p'
old_recommendations = api_calls.get_recommendations_old(token, old_artist_id, old_genre, old_track)
pprint(old_recommendations)

print('--------------------Recommendations')
artist_id = '2VYQTNDsvvKN9wmU5W7xpj'
genre = 'hard rock'
track = '3sxNhARfL8uj7NlMqwF61p'
recommendations = api_calls.get_recommendations(token, artist_id, genre, track)
pprint(recommendations)

print('--------------------50 ARTISTS')
artists_50 = api_calls.get_50_artists(token)
pprint(artists_50)
