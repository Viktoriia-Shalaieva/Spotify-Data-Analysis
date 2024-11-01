import requests
from pprint import pprint

# isrc = "USUM72409273"
#
# url = f"https://musicbrainz.org/ws/2/recording?query=isrc:{isrc}&fmt=json"
#
# response = requests.get(url, headers={"User-Agent": "YourAppName/1.0 (your.email@example.com)"})
#
# data = response.json()
# pprint(data)

isrc_2 = "RUAGW2400908"

url_2 = f"https://musicbrainz.org/ws/2/recording?query=isrc:{isrc_2}&fmt=json"

response_2 = requests.get(url_2, headers={"User-Agent": "YourAppName/1.0 (your.email@example.com)"})

data_2 = response_2.json()
pprint(data_2)
