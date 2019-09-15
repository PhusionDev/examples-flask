from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_file_name = 'serialization_manual_serialization.db'
db_file_path = 'sqlite:///' + os.path.join(basedir, db_file_name)

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = db_file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Movie Model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    director = db.Column(db.String(30))
    year_released = db.Column(db.Integer)


# Create Movie Endpoint
@app.route('/movie', methods=['POST'])
def create_movie():
    data = request.get_json()
    new_movie = Movie(
        title=data['title'],
        director=data['director'],
        year_released=data['year_released']
    )
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({'message': 'movie added!'})


# Get All Movies Endpoint
@app.route('/movie', methods=['GET'])
def get_all_movies():
    movies = Movie.query.all()
    movie_list = []

    # Manual Database Object Serialization
    for movie in movies:
        movie_data = {}
        movie_data['id'] = movie.id
        movie_data['title'] = movie.title
        movie_data['director'] = movie.director
        movie_data['year_released'] = movie.year_released
        movie_list.append(movie_data)

    return jsonify(movie_list)


# Get Single Movie Endpoint
@app.route('/movie/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)

    # Manual Database Object Serialization
    movie_data = {}
    movie_data['id'] = movie.id
    movie_data['title'] = movie.title
    movie_data['director'] = movie.director
    movie_data['year_released'] = movie.year_released

    return jsonify(movie_data)


# Update Movie Endpoint
@app.route('/movie/<movie_id>', methods=['PUT'])
def update_movie(movie_id):
    data = request.get_json()
    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({'error': 'movie not found with that id'})

    # Manual Database Object Serialization
    movie.title = data['title']
    movie.director = data['director']
    movie.year_released = data['year_released']

    db.session.commit()

    return jsonify(
        {
            'updated movie': {
                'id': movie_id,
                'title': data['title'],
                'director': data['director'],
                'year_released': data['year_released']
            }
        }
    )


# Delete Movie Endpoint
@app.route('/movie/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)

    if not movie:
        return jsonify({'error': 'No movie found'})

    db.session.delete(movie)
    db.session.commit()

    return jsonify(
        {
            'deleted movie:': {
                'id': movie_id,
                'title': movie.title,
                'director': movie.director,
                'year_released': movie.year_released
            }
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
