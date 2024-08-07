import unittest
import json
from app import create_app, db
from models import Actor, Movie

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_actors(self):
        res = self.client.get('/actors')
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', str(res.data))

    def test_get_movies(self):
        res = self.client.get('/movies')
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', str(res.data))

    def test_post_actor(self):
        res = self.client.post('/actors', json={
            'name': 'Actor Name',
            'age': 30,
            'gender': 'Male'
        })
        self.assertEqual(res.status_code, 201)
        self.assertIn('id', str(res.data))

    def test_post_movie(self):
        res = self.client.post('/movies', json={
            'title': 'Movie Title',
            'release_date': '2024-01-01'
        })
        self.assertEqual(res.status_code, 201)
        self.assertIn('id', str(res.data))

    def test_patch_actor(self):
        actor = Actor(name='Old Name', age=30, gender='Male')
        db.session.add(actor)
        db.session.commit()
        res = self.client.patch(f'/actors/{actor.id}', json={
            'name': 'New Name'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn('New Name', str(res.data))

    def test_patch_movie(self):
        movie = Movie(title='Old Title', release_date='2024-01-01')
        db.session.add(movie)
        db.session.commit()
        res = self.client.patch(f'/movies/{movie.id}', json={
            'title': 'New Title'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn('New Title', str(res.data))

    def test_delete_actor(self):
        actor = Actor(name='Actor Name', age=30, gender='Male')
        db.session.add(actor)
        db.session.commit()
        res = self.client.delete(f'/actors/{actor.id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', str(res.data))

    def test_delete_movie(self):
        movie = Movie(title='Movie Title', release_date='2024-01-01')
        db.session.add(movie)
        db.session.commit()
        res = self.client.delete(f'/movies/{movie.id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', str(res.data))


if __name__ == '__main__':
    unittest.main()
