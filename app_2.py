import requests
from bs4 import BeautifulSoup

url = 'https://www.chosic.com/list-of-music-genres/'


headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    )
}

response = requests.get(url, headers=headers)
print(response)

soup = BeautifulSoup(response.text, 'html.parser')

# parent_genres = {
#     'Pop': 1,
#     'Electronic': 2,
#     'Hip hop': 3,
#     'R&B': 4,
#     'Latin': 5,
#     'Rock': 6,
#     'Metal': 7,
#     'Country': 8,
#     'Folk/Acoustic': 9,
#     'Classical': 10,
#     'Jazz': 11,
#     'Blues': 12,
#     'Easy listening': 13,
#     'New age': 14,
#     'World/Traditional': 15,
# }


def get_parent_genres(soup_response):
    genres_parent = {}
    d = 1
    for i in soup_response.select(".genre-term-basic"):
        genres_parent[i.text] = d
        d += 1
    return genres_parent


def get_all_subgenres(soup_response, parent_genres_number):
    genre_subgenres = {}

    for main_genre, data_parent_value in parent_genres_number.items():
        subgenre_list = soup_response.find('ul', {'data-parent': str(data_parent_value)})

        subgenres = []
        if subgenre_list:
            # Iterate through all <a> tags with the href attribute in subgenre_list
            for subgenre in subgenre_list.select('.capital-letter.genre-term'):
            # for subgenre in subgenre_list.find_all('a', href=True):
                # Extract the text from the element and remove any extra spaces
                subgenre_name = subgenre.text.strip()
                subgenres.append(subgenre_name)

        genre_subgenres[main_genre] = subgenres

    return genre_subgenres


parent_genres = get_parent_genres(soup)
all_genres_with_subgenres = get_all_subgenres(soup, parent_genres)
print(all_genres_with_subgenres)
