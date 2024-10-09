from source import api_calls
from pprint import pprint
# from source.api_calls import *
# from source.api_calls import get_spotify_access_token


token = api_calls.get_spotify_access_token()
print(token)

marilyn_manson_id = '2VYQTNDsvvKN9wmU5W7xpj'
artist_json_manson = api_calls.get_artist(marilyn_manson_id)
pprint(artist_json_manson)

mm_say10_id = '3sxNhARfL8uj7NlMqwF61p'
track_json_mm_say10 = api_calls.get_track(mm_say10_id)
pprint(track_json_mm_say10)

mm_kill4me_id = '6UIo6YbaXihIZ72MWUpcGb'
market = 'UA'
track_json_mm_say10 = api_calls.get_track_market(mm_kill4me_id, market)
pprint(track_json_mm_say10)