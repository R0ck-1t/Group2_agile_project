import unittest

from sqlalchemy import column, table
import main
import sqlite3
import json
from main import app, db, User
from flask import url_for, request
import flask_login

class MyTestCase(unittest.TestCase):


    def test_random(self):
        """
        Test that random pages return a 404, indicates the the webpage
        is working with regard to routes that are incorrect.
        """
        self.app = app.test_client()
        r = self.app.get('/nonexistant')
        assert r.status_code == 404

    def test_first_example(self):
        """
        Test that the replit page is rendering the correct template.
        """
        self.app = app.test_client()
        r = self.app.get('/view/1')
        self.assertIn('Trivia Game', str(r.data))

    
    def test_usersubmissions(self):
        """
        Test that the user submissions page is rendering the
        correct template.
        """
        self.app = app.test_client()
        r = self.app.get('/submissions')
        self.assertIn('User Submissions', str(r.data))


    def test_account(self):
        """
        Test that the login page renders correctly.
        """
        self.app = app.test_client()
        r = self.app.get("login?next=%2Faccount")
        assert 'Please enter your credentials' in str(r.data)

    
    def test_loaduser(self):

        """
        Test the SQLITE3 database to ensure users can be loaded.
        """

        # Create the path file which contains our database file.
        dbfile = './databases/database.db'

        # Create a SQL connection to our SQLite database.
        con = sqlite3.connect(dbfile)

        # Creating initial cursor.
        cur = con.cursor()

        # Create variable with the list of all users (unencrypted currently).
        table_list = [a for a in cur.execute("SELECT * FROM user")]
        

        # Ensuring the connection is closed.
        con.close()
        self.assertIn("Test", str(table_list))

        
    def test_load_user_id(self):
        """
        Tests the load_user function to ensure it can return
        the correct user.
        """

        self.assertEquals(main.load_user(1).username, 'TestUsername')

    def test_root_redirect(self):
        """
        Tests that the root directory redirects to submissions
        """
        self.app = app.test_client()
        r = self.app.get('/')
        self.assertIn('submissions', str(r.data))


    def test_sign_up(self):
        """
        Tests that the sign up page can be loaded properly.
        """
        self.app = app.test_client()
        r = self.app.get('/signup')
        self.assertIn('sign up credentials', str(r.data))


    def test_test_link(self):
        """
        Tests that the sign up page can be loaded properly.
        """
        self.app = app.test_client()
        r = self.app.get('/test')
        assert r.status_code == 302
