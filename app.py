from flask import abort, Flask, jsonify, request
from flask_cors import CORS
from helpers import validate_schema
from models import Actor, Movie, Performance, setup_db
from sqlalchemy import func


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # ROUTES

    @app.route('/')
    def home():
        '''Handle GET requests'''
        return 'running'

    @app.route('/actors')
    def get_actors():
        '''Handle GET requests for actors'''
        actors = Actor.query.all()
        return jsonify({
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/actors', methods=['POST'])
    def post_actor():
        '''Handle POST requests for actors'''
        body = request.get_json()
        if not validate_schema(body, type='post-actor'):
            abort(422)
        actor = Actor(
            name=body["name"],
            gender=body["gender"],
            age=body["age"]
        )
        actor.insert()
        return jsonify({
            'actor': actor.format()
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def patch_actor(actor_id):
        '''Handle PATCH requests for actors by id'''
        body = request.get_json()
        if not validate_schema(body, type='patch-actor'):
            abort(422)
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        for key in body.keys():
            setattr(actor, key, body[key])
        actor.update()
        return jsonify({
            'actor': actor.format()
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        '''Handle DELETE requests for actors by id'''
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        actor.delete()
        return jsonify({
            'deleted': actor_id
        })

    @app.route('/movies')
    def get_movies():
        '''Handle GET requests for movies'''
        movies = Movie.query.all()
        return jsonify({
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/movies', methods=['POST'])
    def post_movie():
        '''Handle POST requests for movies'''
        body = request.get_json()
        if not validate_schema(body, type='post-movie'):
            abort(422)
        title = body["title"]
        movie = Movie.query.filter(
            func.lower(Movie.title) == title.lower()
        ).first()
        if movie is not None:
            abort(422)
        movie = Movie(
            title=title,
            release_date=body["release_date"]
        )
        movie.insert()
        return jsonify({
            'movie': movie.format()
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def patch_movie(movie_id):
        '''Handle PATCH requests for movies by id'''
        body = request.get_json()
        if not validate_schema(body, type='patch-movie'):
            abort(422)
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        for key in body.keys():
            setattr(movie, key, body[key])
        movie.update()
        return jsonify({
            'movie': movie.format()
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        '''Handle DELETE requests for movies by id'''
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        movie.delete()
        return jsonify({
            'deleted': movie_id
        })

    @app.route('/performances')
    def get_performances():
        '''Handle GET requests for performances'''
        performances = Performance.query.all()
        return jsonify({
            'performances': [performance.format() for performance in performances]
        })

    @app.route('/performances', methods=['POST'])
    def post_performance():
        '''Handle POST requests for performances'''
        body = request.get_json()
        if not validate_schema(body, type='post-performance'):
            abort(422)
        actor_id = body["actor_id"]
        movie_id = body["movie_id"]
        actor = Actor.query.filter(Actor.id == actor_id).first()
        if actor is None:
            abort(422)
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie is None:
            abort(422)
        performance = Performance.query.filter(
            Performance.actor_id == actor_id,
            Performance.movie_id == movie_id
        ).first()
        if performance is not None:
            abort(422)
        performance = Performance(
            actor_id=actor_id,
            movie_id=movie_id
        )
        performance.insert()
        return jsonify({
            'performance': performance.format()
        })

    @app.route('/performances/<int:performance_id>', methods=['DELETE'])
    def delete_performance(performance_id):
        '''Handle DELETE requests for performances by id'''
        performance = Performance.query.get(performance_id)
        if performance is None:
            abort(404)
        performance.delete()
        return jsonify({
            'deleted': performance_id
        })

    # ERROR HANDLERS

    @app.errorhandler(400)
    def bad_request(error):
        '''Handle HTTP 400 errors'''
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        '''Handle HTTP 404 errors'''
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        '''Handle HTTP 422 errors'''
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def internal_server(error):
        '''Handle HTTP 500 errors'''
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run()
