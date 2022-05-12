import unittest
from main import app
from flask import url_for, request

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

    def test_usersubmissions(self):
        """
        Test that the user submissions page is rendering the
        correct template.
        """
        self.app = app.test_client()
        r = self.app.get('/submissions')
        assert 'This is a page for user submissions' in str(r.data)


    def test_account(self):
        self.app = app.test_client()
        r = self.app.get("login?next=%2Faccount")
        assert 'Please enter your credentials' in str(r.data)