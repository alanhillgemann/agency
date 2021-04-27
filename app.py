from flask import Flask, jsonify
from flask_cors import CORS
from models import Actor, Movie, Performance, setup_db


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def home():
        '''Handle GET requests'''
        return 'running'

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run()
