from source import api_calls
from pprint import pprint
# from source.api_calls import *
# from source.api_calls import get_spotify_access_token


token = api_calls.get_spotify_access_token()
print(token)

marilyn_manson_id = '2VYQTNDsvvKN9wmU5W7xpj'
artist_json_manson = api_calls.get_artist(marilyn_manson_id)
pprint(artist_json_manson)

print("App finished")
