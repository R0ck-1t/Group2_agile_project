import unittest
from main import app

class MyTestCase(unittest.TestCase):

    def test_root(self):
        self.app = app.test_client()
        r = self.app.get('/')
        assert r.status_code == 200


    def test_random(self):
        self.app = app.test_client()
        r = self.app.get('/nonexistant')
        assert r.status_code == 404