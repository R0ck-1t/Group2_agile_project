import unittest
from main import app

class MyTestCase(unittest.TestCase):

    def test_root(self):
        """
        Test that the root page is returning the correct status code.
        """
        self.app = app.test_client()
        r = self.app.get('/')
        assert r.status_code == 200


    def test_random(self):
        """
        Test that random pages return a 404, indicates the the webpage
        is working with regard to routes that are incorrect.
        """
        self.app = app.test_client()
        r = self.app.get('/nonexistant')
        assert r.status_code == 404

    def test_replit(self):
        """
        Test that the replit page is rendering the correct template.
        """
        self.app = app.test_client()
        r = self.app.get('/replit')
        assert 'Demo Game' in str(r.data)