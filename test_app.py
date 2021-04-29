import json
import os
import unittest
from app import create_app
from flask_sqlalchemy import SQLAlchemy
from models import Actor, Movie, Performance, setup_db


class AgencyTestCase(unittest.TestCase):
    """Agency test case"""

    def setUp(self):
        """Run before each test"""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Run after each test"""
        pass

    def test_001_success_get_actors(self):
        """Test success GET /actors"""
        response = self.client().get('/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_002_success_post_actors(self):
        """Test success POST /actors"""
        actor = {
            'name': 'Leonardo DiCaprio',
            'gender': 'male',
            'age': '46'
        }
        response = self.client().post('/actors', json=actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_003_error_post_actors_body_not_valid_structure(self):
        """Test error POST /actors when body not valid structure"""
        response = self.client().post('/actors', json=None)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_004_success_patch_actors(self):
        """Test success PATCH /actors"""
        actor = {
            'name': 'Brad Pitt',
            'gender': 'male',
            'age': '57'
        }
        last_actor = Actor.query.order_by(Actor.id.desc()).first()
        response = self.client().patch(
            '/actors/' + str(last_actor.id), json=actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_005_error_patch_actors_by_id_not_exist(self):
        """Test error PATCH /actors/:actor_id when id not exist"""
        response = self.client().delete('/actors/999')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_006_error_patch_actors_body_not_valid_structure(self):
        """Test error PATCH /actors when body not valid structure"""
        last_actor = Actor.query.order_by(Actor.id.desc()).first()
        response = self.client().patch(
            '/actors/' + str(last_actor.id), json=None)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_007_success_get_movies(self):
        """Test success GET /movies"""
        response = self.client().get('/movies')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_008_success_post_movies(self):
        """Test success POST /movies"""
        movie = {
            'title': 'Bullet Train',
            'release_date': '2022-09-23T00:00:00.000Z'
        }
        response = self.client().post('/movies', json=movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_009_error_post_movies_body_not_valid_structure(self):
        """Test error POST /movies when body not valid structure"""
        response = self.client().post('/movies', json=None)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_010_error_post_movies_title_already_exists(self):
        """Test error POST /movies when title already exists"""
        movie = {
            'title': 'Bullet Train',
            'release_date': '2022-09-23T00:00:00.000Z'
        }
        response = self.client().post('/movies', json=movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_011_error_post_movies_release_date_format_not_valid(self):
        """Test error POST /movies when release date format not valid"""
        movie = {
            'title': 'Untitled Movie',
            'release_date': '2022-09-23'
        }
        response = self.client().post('/movies', json=movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_012_error_post_movies_release_date_not_in_future(self):
        """Test error POST /movies when release date format not in future"""
        movie = {
            'title': 'Once Upon A Time...In Hollywood',
            'release_date': '2019-07-26T00:00:00.000Z'
        }
        response = self.client().post('/movies', json=movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_013_success_patch_movies(self):
        """Test success PATCH /movies"""
        movie = {
            'title': 'Bullet Train',
            'release_date': '2022-09-30T00:00:00.000Z'
        }
        last_movie = Movie.query.order_by(Movie.id.desc()).first()
        response = self.client().patch(
            '/movies/' + str(last_movie.id), json=movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_013_error_patch_movies_by_id_not_exist(self):
        """Test error PATCH /movies/:movie_id when id not exist"""
        response = self.client().delete('/movies/999')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_014_error_patch_movies_body_not_valid_structure(self):
        """Test error PATCH /movies when body not valid structure"""
        last_movie = Movie.query.order_by(Movie.id.desc()).first()
        response = self.client().patch(
            '/movies/' + str(last_movie.id), json=None)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_015_error_patch_movies_title_already_exists(self):
        """Test error PATCH /movies when title already exists"""
        movie = Movie(
            title='Blonde',
            release_date='2022-09-30T00:00:00.000Z'
        )
        movie.insert()
        movie_id = movie.id
        movie = {
            'title': 'Bullet Train',
            'release_date': '2022-09-30T00:00:00.000Z'
        }
        response = self.client().patch(
            '/movies/' + str(movie_id), json=movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        movie = Movie.query.order_by(Movie.id.desc()).first()
        movie.delete()

    def test_016_error_post_movies_release_date_format_not_valid(self):
        """Test error POST /movies when release date format not valid"""
        movie = {
            'title': 'Untitled Movie',
            'release_date': '2022-09-23'
        }
        response = self.client().post('/movies', json=movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_017_error_post_movies_release_date_not_in_future(self):
        """Test error POST /movies when release date format not in future"""
        movie = {
            'title': 'Once Upon A Time...In Hollywood',
            'release_date': '2019-07-26T00:00:00.000Z'
        }
        response = self.client().post('/movies', json=movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_018_success_get_performances(self):
        """Test success GET /performances"""
        response = self.client().get('/performances')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_019_success_post_performances(self):
        """Test success POST /performances"""
        last_actor = Actor.query.order_by(Actor.id.desc()).first()
        last_movie = Movie.query.order_by(Movie.id.desc()).first()
        performance = {
            'actor_id': last_actor.id,
            'movie_id': last_movie.id
        }
        response = self.client().post('/performances', json=performance)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_020_error_post_performances_body_not_valid_structure(self):
        """Test error POST /performances when body not valid structure"""
        response = self.client().post('/performances', json=None)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_021_success_delete_performances_by_id(self):
        """Test success DELETE /performances/:performance_id"""
        last_performance = Performance.query.order_by(
            Performance.id.desc()).first()
        response = self.client().delete(
            '/performances/' + str(last_performance.id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_022_error_delete_performances_by_id_not_exist(self):
        """Test error DELETE /performances/:performance_id when id not exist"""
        response = self.client().delete('/performances/999')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_023_success_delete_actors_by_id(self):
        """Test success DELETE /actors/:actor_id"""
        last_actor = Actor.query.order_by(Actor.id.desc()).first()
        response = self.client().delete('/actors/' + str(last_actor.id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_024_error_delete_actors_by_id_not_exist(self):
        """Test error DELETE /actors/:actor_id when id not exist"""
        response = self.client().delete('/actors/999')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_025_success_delete_movies_by_id(self):
        """Test success DELETE /movies/:movie_id"""
        last_movie = Movie.query.order_by(Movie.id.desc()).first()
        response = self.client().delete('/movies/' + str(last_movie.id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_026_error_delete_movies_by_id_not_exist(self):
        """Test error DELETE /movies/:movie_id when id not exist"""
        response = self.client().delete('/movies/999')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')

if __name__ == '__main__':
    unittest.main()
