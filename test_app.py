import json
import os
import unittest
from app import create_app
from flask_sqlalchemy import SQLAlchemy
from models import Actor, Movie, Performance, setup_db

CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRpUExPdXVnN0YwczYzVXlJZ2JjSiJ9.eyJpc3MiOiJodHRwczovL2FsYW5oaWxsZ2VtYW5uLmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDhhNWFlOGI3YjU1NzAwNzI1N2IwZGUiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYxOTY4ODY0MywiZXhwIjoxNjE5Nzc1MDQzLCJhenAiOiJHcTdTVkk5ZDh1ZlJoMjVEcGphRGRxM202NVZDcllMWCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJnZXQ6cGVyZm9ybWFuY2VzIl19.G833dp5Q4DyMzr0aYK5OxT1YRlpYpkc52H4xPdtdgjyImf6o9rC9Jl1KyXdWuq6HbeL8ZHQzfzerpfU5UAlAeo90ahP1SxH-APnERR303WMMbfQx3-j9HOgXuHmT6paKkhfoFV2ZWRlaVOezc2mK6QDPORKa8xr0chQ0giGoLLBxqvzV7MhAAF-xlea3ON7hlOWY4ACkAhMtTmxObfc4dOQVEvXwlfLAvA6JvRZMi5PhUSMTDLtTpAzIpbzbCDdaFN7PgVXlcfFDeB1RFIOZBrTA_Cf4vgu37LHhCydJXyypRWOIcPSrnn41xQKbP1UjDDNZNEXHQunuEGYcEnuJRQ'  # noqa
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRpUExPdXVnN0YwczYzVXlJZ2JjSiJ9.eyJpc3MiOiJodHRwczovL2FsYW5oaWxsZ2VtYW5uLmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDhhNWIwYWI3YjU1NzAwNzI1N2IwZTUiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYxOTc0NzU0NSwiZXhwIjoxNjE5ODMzOTQ1LCJhenAiOiJHcTdTVkk5ZDh1ZlJoMjVEcGphRGRxM202NVZDcllMWCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTpwZXJmb3JtYW5jZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsImdldDpwZXJmb3JtYW5jZXMiLCJwYXRjaDphY3RvcnMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6cGVyZm9ybWFuY2VzIl19.lSYoT0P2VlmGu41yhNqSBKE8Y5YYma5g_rxTfMXJrBDt_6c3a3HApibtOvBoAYFyvWoY4R1jUzZFzEZVG390BacBaaIJsAkMwKBFtTFKKmTuTd04TBKfdXvwIaQYTpxLEN83C_iRgD6zP0W2PhBu1BaZaJHbvaeYu-SmT9eLXxIShcY2rkPHRsxxXlsWrIt5wkilcL1XiCCw8ckNM6Ng4uCgtsdtGqrduWUUqWpolg_EXuQWxA1qI983FVfcAgBoyIZFVMnEFCS4Q9AO5NBrlaa-HlGnQDQyX528_Hzu83TNavIvmOgaKrKTqQxZ5lSFuQmlv_UCIp-okZr08A41rg'  # noqa
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImRpUExPdXVnN0YwczYzVXlJZ2JjSiJ9.eyJpc3MiOiJodHRwczovL2FsYW5oaWxsZ2VtYW5uLmF1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDhhNWI0ZmMzNzQ5ODAwNjg0OGNjYjkiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYxOTY4NDcwMCwiZXhwIjoxNjE5NzcxMTAwLCJhenAiOiJHcTdTVkk5ZDh1ZlJoMjVEcGphRGRxM202NVZDcllMWCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJkZWxldGU6cGVyZm9ybWFuY2VzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJnZXQ6cGVyZm9ybWFuY2VzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyIsInBvc3Q6cGVyZm9ybWFuY2VzIl19.SblDHXLwmOlWbQZ2BuoyzxZ7_n1aMjsJglSyBaHlK-VMjy35XUHhC8jFq7nFYAi2JDBmGsOBjWVNgOHYHiE120YPQaP3ZXdJoVQrh-OrdS7zaG4AJmB80iCSqo8FyLxhrNVNpAWoWngl68eVYp_vBAH4yCoJMFT-1ffNd_ox3lOPGzNRUGuiCOhETkDQsG2L6Hep_LNhgcyaGHWnj__0y__0X3fEjDll20ybsFWrGU-oiuTHmphzTdigXbm-GbE_KIjyuK4a1eX2KTqK3_aYaQtDn49jUrBo88OWpFkeNHAS9l1SwrIhsog7Z256Zn8hWLDkT3j7_4uh-1OSinTY_A'  # noqa


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
        response = self.client().get(
            '/actors',
            headers={'Authorization': 'Bearer ' + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_002_success_post_actors(self):
        """Test success POST /actors"""
        actor = {
            'name': 'Leonardo DiCaprio',
            'gender': 'male',
            'age': '46'
        }
        response = self.client().post(
            '/actors',
            json=actor,
            headers={'Authorization': 'Bearer ' + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_003_error_post_actors_body_not_valid_structure(self):
        """Test error POST /actors when body not valid structure"""
        response = self.client().post(
            '/actors',
            json=None,
            headers={'Authorization': 'Bearer ' + CASTING_DIRECTOR}
        )
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
            '/actors/' + str(last_actor.id),
            json=actor,
            headers={'Authorization': 'Bearer ' + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_005_error_patch_actors_by_id_not_exist(self):
        """Test error PATCH /actors/:actor_id when id not exist"""
        response = self.client().delete(
            '/actors/999',
            headers={'Authorization': 'Bearer ' + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_006_error_patch_actors_body_not_valid_structure(self):
        """Test error PATCH /actors when body not valid structure"""
        last_actor = Actor.query.order_by(Actor.id.desc()).first()
        response = self.client().patch(
            '/actors/' + str(last_actor.id),
            json=None,
            headers={'Authorization': 'Bearer ' + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_007_success_get_movies(self):
        """Test success GET /movies"""
        response = self.client().get(
            '/movies',
            headers={'Authorization': 'Bearer ' + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_008_success_post_movies(self):
        """Test success POST /movies"""
        movie = {
            'title': 'Bullet Train',
            'release_date': '2022-09-23T00:00:00.000Z'
        }
        response = self.client().post(
            '/movies',
            json=movie,
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_009_error_post_movies_body_not_valid_structure(self):
        """Test error POST /movies when body not valid structure"""
        response = self.client().post(
            '/movies',
            json=None,
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_010_error_post_movies_title_already_exists(self):
        """Test error POST /movies when title already exists"""
        movie = {
            'title': 'Bullet Train',
            'release_date': '2022-09-23T00:00:00.000Z'
        }
        response = self.client().post(
            '/movies',
            json=movie,
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_011_error_post_movies_release_date_format_not_valid(self):
        """Test error POST /movies when release date format not valid"""
        movie = {
            'title': 'Untitled Movie',
            'release_date': '2022-09-23'
        }
        response = self.client().post(
            '/movies',
            json=movie,
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_012_error_post_movies_release_date_not_in_future(self):
        """Test error POST /movies when release date format not in future"""
        movie = {
            'title': 'Once Upon A Time...In Hollywood',
            'release_date': '2019-07-26T00:00:00.000Z'
        }
        response = self.client().post(
            '/movies',
            json=movie,
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
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
            '/movies/' + str(last_movie.id),
            json=movie,
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_013_error_patch_movies_by_id_not_exist(self):
        """Test error PATCH /movies/:movie_id when id not exist"""
        response = self.client().delete(
            '/movies/999',
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_014_error_patch_movies_body_not_valid_structure(self):
        """Test error PATCH /movies when body not valid structure"""
        last_movie = Movie.query.order_by(Movie.id.desc()).first()
        response = self.client().patch(
            '/movies/' + str(last_movie.id),
            json=None,
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
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
            '/movies/' + str(movie_id),
            json=movie,
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
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
        response = self.client().post(
            '/movies',
            json=movie,
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_017_error_post_movies_release_date_not_in_future(self):
        """Test error POST /movies when release date format not in future"""
        movie = {
            'title': 'Once Upon A Time...In Hollywood',
            'release_date': '2019-07-26T00:00:00.000Z'
        }
        response = self.client().post(
            '/movies',
            json=movie,
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_018_success_get_performances(self):
        """Test success GET /performances"""
        response = self.client().get(
            '/performances',
            headers={'Authorization': 'Bearer ' + CASTING_ASSISTANT}
        )
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
        response = self.client().post(
            '/performances',
            json=performance,
            headers={'Authorization': 'Bearer ' + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_020_error_post_performances_body_not_valid_structure(self):
        """Test error POST /performances when body not valid structure"""
        response = self.client().post(
            '/performances',
            json=None,
            headers={'Authorization': 'Bearer ' + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_021_success_delete_performances_by_id(self):
        """Test success DELETE /performances/:performance_id"""
        last_performance = Performance.query.order_by(
            Performance.id.desc()).first()
        response = self.client().delete(
            '/performances/' + str(last_performance.id),
            headers={'Authorization': 'Bearer ' + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_022_error_delete_performances_by_id_not_exist(self):
        """Test error DELETE /performances/:performance_id when id not exist"""
        response = self.client().delete(
            '/performances/999',
            headers={'Authorization': 'Bearer ' + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_023_success_delete_actors_by_id(self):
        """Test success DELETE /actors/:actor_id"""
        last_actor = Actor.query.order_by(Actor.id.desc()).first()
        response = self.client().delete(
            '/actors/' + str(last_actor.id),
            headers={'Authorization': 'Bearer ' + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_024_error_delete_actors_by_id_not_exist(self):
        """Test error DELETE /actors/:actor_id when id not exist"""
        response = self.client().delete(
            '/actors/999',
            headers={'Authorization': 'Bearer ' + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_025_success_delete_movies_by_id(self):
        """Test success DELETE /movies/:movie_id"""
        last_movie = Movie.query.order_by(Movie.id.desc()).first()
        response = self.client().delete(
            '/movies/' + str(last_movie.id),
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_026_error_delete_movies_by_id_not_exist(self):
        """Test error DELETE /movies/:movie_id when id not exist"""
        response = self.client().delete(
            '/movies/999',
            headers={'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')

if __name__ == '__main__':
    unittest.main()
