import requests
from bs4 import BeautifulSoup


def get_genres():
    url = "https://www.chosic.com/list-of-music-genres/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    genres_parent = {}
    d = 1
    for i in soup.select(".genre-term-basic"):
        genres_parent[i.text] = d
        d += 1

    genre_subgenres = {}

    for main_genre, data_parent_value in genres_parent.items():
        subgenre_list = soup.find("ul", {"data-parent": str(data_parent_value)})

        subgenres = []
        if subgenre_list:
            # Iterate through all <a> tags with the href attribute in subgenre_list
            for subgenre in subgenre_list.select(".capital-letter.genre-term"):
                # for subgenre in subgenre_list.find_all("a", href=True):
                # Extract the text from the element and remove any extra spaces
                subgenre_name = subgenre.text.strip()
                subgenres.append(subgenre_name)

        genre_subgenres[main_genre] = subgenres

    return genre_subgenres
