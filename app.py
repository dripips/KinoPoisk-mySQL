import requests
import mysql.connector
from mysql.connector import Error
import json

# Функция для получения данных о фильме из Kinopoisk API
def get_movie_data(kinopoisk_id, api_key):
    api_url = f"https://api.kinopoisk.dev/v1.3/movie/{kinopoisk_id}"
    headers = {"X-API-KEY": api_key}

    # Используем параметр stream для получения сырых данных
    response = requests.get(api_url, headers=headers)
    print(response)
    if response.status_code == 200:
        print(response.json())
        return response.json()

    else:
        print(f"Не удалось получить данные для kinopoiskId {kinopoisk_id}")
        return None

# Функция для вставки данных фильма в базу данных MySQL
def insert_movie_data(movie_data, cursor):
    sql = """
    INSERT INTO n_movies (
        `id`, `externalIdKpHD`, `externalIdImdb`, `externalIdTmdb`, `name`, `alternativeName`, `enName`, `names`, `type`, `typeNumber`, `year`, `description`, `shortDescription`, `slogan`, `status`, `ratingKp`, `ratingImdb`, `ratingTmdb`, `ratingFilmCritics`, `ratingRussianFilmCritics`, `ratingAwait`, `votesKp`, `votesImdb`, `votesTmdb`, `votesFilmCritics`, `votesRussianFilmCritics`, `votesAwait`, `movieLength`, `ratingMpaa`, `ageRating`, `poster`, `videos`, `genres`, `countries`, `persons`, `premiere`, `top10`, `top250`, `ticketsOnSale`, `totalSeriesLength`, `seriesLength`, `isSeries`, `seasonsInfo`
    ) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """
    seasons_info = movie_data.get("seasonsInfo")
    seasons_info_json = json.dumps(seasons_info) if seasons_info is not None else None
    values = (
        movie_data["id"],
        movie_data["externalId"].get("kpHD", None),
        movie_data["externalId"].get("imdb", None),
        movie_data["externalId"].get("tmdb", None),
        movie_data["name"],
        movie_data.get("alternativeName", None),
        movie_data.get("enName", None),
        ', '.join(f'{name["name"]}:{name.get("language", "N/A")}' for name in movie_data.get("names", [])) if "names" in movie_data else None,
        movie_data.get("type", None),
        movie_data.get("typeNumber", None),
        movie_data.get("year", None),
        movie_data.get("description", None),
        movie_data.get("shortDescription", None),
        movie_data.get("slogan", None),
        movie_data.get("status", None),
        movie_data["rating"].get("kp", None) if "rating" in movie_data else None,
        movie_data["rating"].get("imdb", None) if "rating" in movie_data else None,
        movie_data["rating"].get("tmdb", None) if "rating" in movie_data else None,
        movie_data["rating"].get("filmCritics", None) if "rating" in movie_data else None,
        movie_data["rating"].get("russianFilmCritics", None) if "rating" in movie_data else None,
        movie_data["rating"].get("await", None) if "rating" in movie_data else None,
        movie_data["votes"].get("kp", None) if "votes" in movie_data else None,
        movie_data["votes"].get("imdb", None) if "votes" in movie_data else None,
        movie_data["votes"].get("tmdb", None) if "votes" in movie_data else None,
        movie_data["votes"].get("filmCritics", None) if "votes" in movie_data else None,
        movie_data["votes"].get("russianFilmCritics", None) if "votes" in movie_data else None,
        movie_data["votes"].get("await", None) if "votes" in movie_data else None,
        movie_data.get("movieLength", None),
        movie_data.get("ratingMpaa", None),
        movie_data.get("ageRating", None),
        json.dumps(movie_data["poster"]) if "poster" in movie_data else None,
        json.dumps(movie_data["videos"]) if "videos" in movie_data else None,
        json.dumps([{"name": genre["name"]} for genre in movie_data.get("genres", [])]) if "genres" in movie_data else None,
        json.dumps([{"name": country["name"]} for country in movie_data.get("countries", [])]) if "countries" in movie_data else None,
        json.dumps([{
            "id": person["id"],
            "photo": person.get("photo", None),
            "name": person.get("name", None),
            "enName": person.get("enName", None),
            "description": person.get("description", None),
            "profession": person.get("profession", None),
            "enProfession": person.get("enProfession", None)
        } for person in movie_data.get("persons", [])]) if "persons" in movie_data else None,
        json.dumps(movie_data["premiere"]) if "premiere" in movie_data else None,
        movie_data.get("top10", None),
        movie_data.get("top250", None),
        movie_data.get("ticketsOnSale", None),
        movie_data.get("totalSeriesLength", None),
        movie_data.get("seriesLength", None),
        movie_data.get("isSeries", None),
        seasons_info_json
    )

    cursor.execute(sql, values)


# Подключение к базе данных MySQL
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="",
        password="",
        database=""
    )

    if connection.is_connected():
        cursor = connection.cursor()

        for kinopoisk_id in range(490, 99999999):

            api_key = "ТУТ КЛЮЧ"
            movie_data = get_movie_data(kinopoisk_id, api_key)
            if movie_data:
                insert_movie_data(movie_data, cursor)
                connection.commit()

except Error as e:
    print(f"Ошибка при работе с базой данных: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Соединение с базой данных закрыто")
