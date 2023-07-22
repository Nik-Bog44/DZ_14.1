import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)


def get_movie_data(title):
    con = sqlite3.connect("../netflix.db")
    cur = con.cursor()
    sqlite_query = f"SELECT title, country, release_year, listed_in, description " \
                   f"FROM netflix WHERE title LIKE '%{title}%' " \
                   f"ORDER BY release_year DESC LIMIT 1"
    cur.execute(sqlite_query)
    data = cur.fetchone()
    con.close()
    return data


def format_movie_data(data):
    if data:
        title, country, release_year, genre, description = data
        movie_data = {
            "title": title,
            "country": country,
            "release_year": release_year,
            "genre": genre,
            "description": description
        }
        return movie_data
    return None


def get_movies_by_year_range(start_year, end_year):
    con = sqlite3.connect("../netflix.db")
    cur = con.cursor()
    sqlite_query = "SELECT title, release_year FROM netflix WHERE release_year BETWEEN 2020 AND 2021 LIMIT 100"
    cur.execute(sqlite_query, (start_year, end_year))
    data = cur.fetchall()
    con.close()
    return data


def format_movie_data(data):
    formatted_data = []
    for title, release_year in data:
        formatted_data.append({
            "title": title,
            "release_year": release_year
        })
    return formatted_data


def get_movies_by_rating(rating_group):
    con = sqlite3.connect("../netflix.db")
    cur = con.cursor()
    sqlite_query = "SELECT title, rating, description FROM netflix WHERE rating IN ({})".format(
        ','.join('?' * len(rating_group)))
    cur.execute(sqlite_query, rating_group)
    data = cur.fetchall()
    con.close()
    return data


def format_movie_data(data):
    formatted_data = []
    for title, rating, description in data:
        formatted_data.append({
            "title": title,
            "rating": rating,
            "description": description
        })
    return formatted_data


def get_movies_by_genre(genre):
    con = sqlite3.connect("../netflix.db")
    cur = con.cursor()
    sqlite_query = "SELECT title, description FROM netflix " \
                   "WHERE genre LIKE '%' || ? || '%' " \
                   "ORDER BY release_year DESC LIMIT 10"
    cur.execute(sqlite_query, (genre,))
    data = cur.fetchall()
    con.close()
    return data


def get_actors_in_pair(actor1, actor2):
    con = sqlite3.connect("../netflix.db")
    cur = con.cursor()

    # Находим всех актеров, которые снимались с actor1
    cur.execute("SELECT cast FROM netflix WHERE cast LIKE ?", ('%' + actor1 + '%',))
    movies_with_actor1 = cur.fetchall()

    # Находим всех актеров, которые снимались с actor2
    cur.execute("SELECT cast FROM netflix WHERE cast LIKE ?", ('%' + actor2 + '%',))
    movies_with_actor2 = cur.fetchall()

    con.close()

    # Объединяем актеров из двух списков
    actors_with_actor1 = set()
    for movie in movies_with_actor1:
        actors_with_actor1.update(movie[0].split(','))

    actors_with_actor2 = set()
    for movie in movies_with_actor2:
        actors_with_actor2.update(movie[0].split(','))

    # Находим актеров, которые снимались с обоими заданными актерами (actor1 и actor2)
    common_actors = actors_with_actor1.intersection(actors_with_actor2)

    # Фильтруем актеров, считая, сколько раз каждый из них снимался с actor1 и actor2
    actors_in_pair_more_than_2_times = []
    for actor in common_actors:
        count_with_actor1 = sum(movie[0].count(actor) for movie in movies_with_actor1)
        count_with_actor2 = sum(movie[0].count(actor) for movie in movies_with_actor2)
        total_count = count_with_actor1 + count_with_actor2
        if total_count > 2:
            actors_in_pair_more_than_2_times.append(actor)

    return actors_in_pair_more_than_2_times


def get_movies_by_type_year_genre(movie_type, release_year, genre):
    con = sqlite3.connect("../netflix.db")
    cur = con.cursor()
    sqlite_query = "SELECT title, description FROM netflix WHERE type = ? AND release_year = ? AND genre LIKE '%' || ? || '%'"
    cur.execute(sqlite_query, (movie_type, release_year, genre))
    data = cur.fetchall()
    con.close()
    return data


def format_movie_data(data):
    formatted_data = []
    for title, description in data:
        formatted_data.append({
            "title": title,
            "description": description
        })
    return formatted_data


@app.route('/movie/<title>')
def movie_details(title):
    movie_data = get_movie_data(title)
    if movie_data:
        formatted_data = format_movie_data(movie_data)
        return jsonify(formatted_data)
    else:
        return jsonify({"message": "Фильм не найден"}), 404


@app.route('/movie/<int:start_year>/to/<int:end_year>')
def movies_by_year_range(start_year, end_year):
    movie_data = get_movies_by_year_range(start_year, end_year)
    formatted_data = format_movie_data(movie_data)
    return jsonify(formatted_data)


@app.route('/rating/children')
def children_rating_movies():
    rating_group = ['G']
    movie_data = get_movies_by_rating(rating_group)
    formatted_data = format_movie_data(movie_data)
    return jsonify(formatted_data)


@app.route('/rating/family')
def family_rating_movies():
    rating_group = ['G', 'PG', 'PG-13']
    movie_data = get_movies_by_rating(rating_group)
    formatted_data = format_movie_data(movie_data)
    return jsonify(formatted_data)


@app.route('/rating/adult')
def adult_rating_movies():
    rating_group = ['R', 'NC-17']
    movie_data = get_movies_by_rating(rating_group)
    formatted_data = format_movie_data(movie_data)
    return jsonify(formatted_data)


def format_movie_data(data):
    formatted_data = []
    for title, description in data:
        formatted_data.append({
            "title": title,
            "description": description
        })
    return formatted_data


@app.route('/genre/<genre>')
def movies_by_genre(genre):
    movie_data = get_movies_by_genre(genre)
    formatted_data = format_movie_data(movie_data)
    return jsonify(formatted_data)


if __name__ == '__main__':
    app.run(debug=True)
