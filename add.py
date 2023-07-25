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


@app.route('/genre/<genre>')
def movies_by_genre(genre):
    movie_data = get_movies_by_genre(genre)
    formatted_data = format_movie_data(movie_data)
    return jsonify(formatted_data)





if __name__ == '__main__':
    app.run(debug=True)
