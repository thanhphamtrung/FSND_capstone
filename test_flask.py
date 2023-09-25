import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Casting, Actor


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.JWT = os.getenv('JWT', '')
        self.AUTH_HEADER = { 'Authorization': 'Bearer {}'.format(self.JWT) }
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_NAME = os.getenv('DB_NAME', 'casting-agency')
        DB_PATH = 'postgresql://{}@{}/{}'.format(DB_USER, DB_HOST, DB_NAME)
        setup_db(self.app, DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies_200(self):
        '''
            Test getting movies successfully
        '''
        res = self.client().get("/movies", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_get_movies_404(self):
        '''
            Test getting movies failed
        '''
        res = self.client().get("/movies?page=100", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_movies_401(self):
        '''
            Test getting movies without authorization
        '''
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_search_movies_200(self):
        '''
            Test searching movies successfully
        '''
        res = self.client().get("/movies?searchTerm=Dune", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_search_movies_404(self):
        '''
            Test searching movies failed
        '''
        res = self.client().get("/movies?searchTerm=zxcvzcv", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_search_movies_401(self):
        '''
            Test searching movies without authorization
        '''
        res = self.client().get("/movies?searchTerm=Jeff")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_patch_movies_200(self):
        '''
            Test updating movie successfully
        '''
        # Create a test movie
        movie = Movie(name='Test movie')
        movie.insert()

        data = {
            'name': 'Updated movie',
            'producer': 'Tom',
            'director': 'Tim',
            'phone': '3333333',
            'genres': 'Action'
        }
        res = self.client().patch("/movies/{}".format(movie.id), content_type='multipart/form-data', data=data, headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
        movie.delete()

    def test_patch_movies_error(self):
        '''
            Test updating movie failed
        '''
        # Create a test movie
        movie = Movie(name='Test movie')
        movie.insert()

        res = self.client().patch("/movies/{}".format(movie.id), headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual("Form format error." in data["message"], True)
        
        movie.delete()

    def test_patch_movies_401(self):
        '''
            Test updating movie without authorization
        '''
        # Create a test movie
        movie = Movie(name='Test movie')
        movie.insert()

        data = {
            'name': 'Updated movie',
            'producer': 'Tom',
            'director': 'Tim',
            'phone': '3333333',
            'genres': 'Action'
        }
        res = self.client().patch("/movies/{}".format(movie.id), content_type='multipart/form-data', data=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
        movie.delete()

    def test_create_movies_200(self):
        '''
            Test creating movie successfully
        '''
        data = {
            'name': 'New movie',
            'producer': 'Tom',
            'director': 'Tim',
            'phone': '3333333',
            'genres': 'Action'
        }
        res = self.client().post("/movies", content_type='multipart/form-data', data=data, headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        if data["success"]:
            last_movie = Movie.query.order_by(Movie.id.desc()).first()
            last_movie.delete()

    def test_create_movies_error(self):
        '''
            Test creating movie failed
        '''
        data = {
            'name': 'New movie',
        }
        res = self.client().post("/movies", content_type='multipart/form-data', data=data, headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual("Form format error." in data["message"], True)

    def test_delete_movies_200(self):
        '''
            Test updating movie successfully
        '''
        # Create a test movie
        movie = Movie(name='Test movie')
        movie.insert()

        res = self.client().delete("/movies/{}".format(movie.id), headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_delete_movies_404(self):
        '''
            Test updating movie failed
        '''
        res = self.client().delete("/movies/100", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_movies_200(self):
        '''
            Test updating movie successfully
        '''
        # Create a test movie
        movie = Movie(name='Test movie')
        movie.insert()

        res = self.client().delete("/movies/{}".format(movie.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
        movie.delete()

    def test_get_actors_200(self):
        '''
            Test getting actors successfully
        '''
        res = self.client().get("/actors", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_get_actors_404(self):
        '''
            Test getting actors failed
        '''
        res = self.client().get("/actors?page=100", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_actors_401(self):
        '''
            Test getting actors without authorization
        '''
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_search_actors_200(self):
        '''
            Test searching actors successfully
        '''
        res = self.client().get("/actors?searchTerm=Jeff", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_search_actors_404(self):
        '''
            Test searching actors failed
        '''
        res = self.client().get("/actors?searchTerm=zxcvzcv", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_search_actors_401(self):
        '''
            Test searching actors without authorization
        '''
        res = self.client().get("/actors?searchTerm=Jeff")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_patch_actors_200(self):
        '''
            Test updating actors successfully
        '''
        # Create a test actor
        actor = Actor(name='Test actor')
        actor.insert()

        data = {
            'name': 'Updated actor',
            'age': '30',
            'sex': 'Male',
            'phone': '3333333',
            'genres': 'Action',
            'state': 'AL'
        }
        res = self.client().patch("/actors/{}".format(actor.id), content_type='multipart/form-data', data=data, headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
        actor.delete()
        
    def test_patch_actor_error(self):
        '''
            Test updating actor failed
        '''
        # Create a test actor
        actor = Movie(name='Test actor')
        actor.insert()

        res = self.client().patch("/actors/{}".format(actor.id), headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual("Form format error." in data["message"], True)
        
        actor.delete()
    
    def test_patch_actor_401(self):
        '''
            Test updating actor without authorization
        '''
        # Create a test actor
        actor = Movie(name='Test actor')
        actor.insert()

        data = {
            'name': 'Updated movie',
            'producer': 'Tom',
            'director': 'Tim',
            'phone': '3333333',
            'genres': 'Action',
            'state': 'AL'
        }
        res = self.client().patch("/movies/{}".format(actor.id), content_type='multipart/form-data', data=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        
        actor.delete()

    def test_create_actor_200(self):
        '''
            Test creating actor successfully
        '''
        data = {
            'name': 'Updated actor',
            'age': '30',
            'sex': 'Male',
            'phone': '3333333',
            'genres': 'Action',
            'state': 'AL'
        }
        res = self.client().post("/actors", content_type='multipart/form-data', data=data, headers=self.AUTH_HEADER)
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        if data["success"]:
            last_actor = Actor.query.order_by(Actor.id.desc()).first()
            last_actor.delete()
 
    def test_create_actor_error(self):
        '''
            Test creating actor failed
        '''
        data = {
            'name': 'New actor',
        }
        res = self.client().post("/actors", content_type='multipart/form-data', data=data, headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual("Form format error." in data["message"], True)
    
    def test_create_actor_401(self):
        '''
            Test updating actor without authorization
        '''
        data = {
            'name': 'Updated actor',
            'age': '30',
            'sex': 'Male',
            'phone': '3333333',
            'genres': 'Action',
            'state': 'AL'
        }
        res = self.client().post("/actors", content_type='multipart/form-data', data=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_delete_actor_200(self):
        '''
            Test updating actor successfully
        '''
        # Create a test movie
        actor = Actor(name='Test actor')
        actor.insert()

        res = self.client().delete("/actors/{}".format(actor.id), headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_delete_actor_404(self):
        '''
            Test updating actor failed
        '''
        res = self.client().delete("/actors/100", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
    
    def test_delete_actor_401(self):
        '''
            Test updating actor successfully
        '''
        # Create a test actor
        actor = Actor(name='Test actor')
        actor.insert()

        res = self.client().delete("/movies/{}".format(actor.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
        actor.delete()

    def test_get_castings_200(self):
        '''
            Test getting castings successfully
        '''
        res = self.client().get("/castings", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["castings"]))

    def test_get_castings_404(self):
        '''
            Test getting castings failed
        '''
        res = self.client().get("/castings?page=100", headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_castings_401(self):
        '''
            Test getting castings without authorization
        '''
        res = self.client().get("/castings")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)        

    def test_create_casting_200(self):
        '''
            Test creating casting successfully
        '''
        data = {
            'actor_id': '1',
            'movie_id': '1',
            'start_time': '2014-12-11 23:30:34',
            'place': '342street'
        }
        res = self.client().post("/castings", content_type='multipart/form-data', data=data, headers=self.AUTH_HEADER)
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        if data["success"]:
            last_casting = Casting.query.order_by(Casting.id.desc()).first()
            last_casting.delete()
 
    def test_create_casting_error(self):
        '''
            Test creating casting successfully
        '''
        data = {
            'actor_id': '1',
        }
        res = self.client().post("/castings", content_type='multipart/form-data', data=data, headers=self.AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual("Form format error." in data["message"], True)
    
    def test_create_actor_401(self):
        '''
            Test creating casting successfully
        '''
        data = {
            'actor_id': '1',
            'movie_id': '1',
            'start_time': '2014-12-11 23:30:34',
            'place': '342street'
        }
        res = self.client().post("/castings", content_type='multipart/form-data', data=data)
        data = json.loads(res.data)

        if data["success"]:
            last_casting = Casting.query.order_by(Casting.id.desc()).first()
            last_casting.delete()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()