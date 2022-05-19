import unittest
import pytest

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
        assert 'Submit New Replit' in str(r.data)


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
        self.assertIn("JustinTan", str(table_list))


    def test_to_dict(self):
        """
        Tests that the function currently returns the
        amount of users in the database, in dictionary format.
        """
        dict_data = main.to_dict()
        self.assertEqual(len(dict_data), 4)

    def test_debugger_user(self):
        """
        Tests that a default user exists which can allow
        developers to debugg and troubleshoot the database.
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

        # Find the debugger user account
        found_user = False
        for user in table_list:
            if user[1] == "TestUsername" and user[2] == "TestEmailAgile@scrum.ca":
                found_user = True
                break
        
        # Check that the user is found
        self.assertTrue(found_user)
        
    pytest.exit()
    py.test.exit()
