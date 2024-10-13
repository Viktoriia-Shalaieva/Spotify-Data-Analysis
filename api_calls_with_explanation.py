import requests


def get_spotify_access_token():
    client_id = 'ac3eaf00cb0845a8a8a2f60c134c328e'
    client_secret = 'bc63f9adbb3a4bea8e5c7ba13b951e8e'

    token_url = "https://accounts.spotify.com/api/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(
        token_url,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    token_info = response.json()
    access_token = token_info.get("access_token")

    return access_token


def get_artist(artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    # Коли ми надсилаємо HTTP-запит за допомогою бібліотеки requests, сервер (Spotify API)
    # повертає відповідь з певним статус-кодом. Цей код дає інформацію про те, як оброблений наш запит.
    # 200 OK означає, що все пройшло добре, і ми можемо працювати з отриманими даними.
    # Інші статус-коди, наприклад, 404 Not Found (не знайдено) або 401 Unauthorized (недостатньо прав), вказують на те, що щось пішло не так.
    # Check the status code
    if response.status_code == 200:
        artist_info = response.json()
        print("Artist information retrieved successfully:")
        return artist_info

    # Якщо статус-код не 200 (тобто відповідь неуспішна), використовуємо блок else, щоб обробити ситуацію, коли сталася помилка
    else:
        # If not successful, print the status code and error message
        print(f"Error: Received status code {response.status_code}")
        # Іноді сервер повертає відповідь, яка не містить правильних даних у форматі JSON. Наприклад,
        # сервер може повернути помилку без JSON або навіть взагалі без тексту.
        # У таких випадках виклик response.json() може викликати виняток (помилку виконання).
        # Щоб обробити такі випадки без "падіння" програми, ми використовуємо конструкцію try-except
        try:
            error_info = response.json()
            print("Error details:", error_info)
        # except: Якщо сталася помилка (наприклад, якщо відповіді немає або вона не в JSON-форматі),
        # ми перехоплюємо виняток і замість "падіння" програми виводимо зрозуміле повідомлення.
        # У блоці except краще прописувати лише ту частину коду, яка чітко обробляє очікувані винятки та
        # допомагає надати корисну інформацію про помилку. Це важливо, щоб програма не "падала" через
        # неконтрольовані винятки, але при цьому користувач або розробник могли зрозуміти, що сталося, і як це виправити.
        # ValueError - помилка через неправильний формат JSON
        # requests.exceptions.RequestException- загальний виняток для всіх інших помилок, пов'язаних із запитами.

        # ЧИ ВАРТО ПРОПИСУВАТИ для обробки requests.exceptions.RequestException?????? Мені здається, що не варто
        # (так як я не зможу відрізнити різні типи помилок), але уточнити!!!!!!!!!!
        # ДОДАТКОВО ПОЧИТАТИ ПРО ОБРОБКУ ПОМИЛОК!!!!!!! Можливо, варто додати ще до обробки винятків
        except ValueError:
            print("No JSON response received.")
        return None


def get_track(track_id, access_token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    track_info = response.json()
    return track_info

def get_track_market(track_id, market, access_token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}?market={market}"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    track_info = response.json()
    return track_info

def get_album(album_id, access_token):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    album_info = response.json()
    return album_info
