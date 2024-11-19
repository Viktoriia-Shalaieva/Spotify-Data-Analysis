import requests
from pprint import pprint


api_token = "32f003350629bc0ef36103d8ab84ced4"
isrc = "USUM72409273"
return_data = "apple_music,spotify"

url = f"https://api.audd.io/?isrc={isrc}&return={return_data}&api_token={api_token}"

response = requests.get(url)

data = response.json()
pprint(data)
