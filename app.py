from flask import abort, Flask, jsonify, request
from flask_cors import CORS
from helpers import validate_schema
from models import Actor, Movie, Performance, setup_db


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
