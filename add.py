from flask import Flask, jsonify

from main import get_movie_data, get_movies_by_year_range, get_movies_by_rating, get_movies_by_genre, format_movie_data

app = Flask(__name__)


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
    data = []
    for elem in movie_data:
        data.append({'title': elem[0], 'year': elem[1]})
    return jsonify(data)


@app.route('/rating/children')
def children_rating_movies():
    rating_group = ['G']
    movie_data = get_movies_by_rating(rating_group)
    data = []
    for elem in movie_data:
        data.append({'title': elem[0], 'rating': elem[1], 'description': elem[2]})
    return jsonify(data)


@app.route('/rating/family')
def family_rating_movies():
    rating_group = ['G', 'PG', 'PG-13']
    movie_data = get_movies_by_rating(rating_group)
    data = []
    for elem in movie_data:
        data.append({'title': elem[0], 'rating': elem[1], 'description': elem[2]})
    return jsonify(data)


@app.route('/rating/adult')
def adult_rating_movies():
    rating_group = ['R', 'NC-17']
    movie_data = get_movies_by_rating(rating_group)
    data = []
    for elem in movie_data:
        data.append({'title': elem[0], 'rating': elem[1], 'description': elem[2]})
    return jsonify(data)


@app.route('/genre/<genre>')
def movies_by_genre(genre):
    movie_data = get_movies_by_genre(genre)
    data = []
    for elem in movie_data:
        data.append({'title': elem[0], 'description': elem[1], 'genre': elem[2]})
    return jsonify(data)





if __name__ == '__main__':
    app.run(debug=True)
