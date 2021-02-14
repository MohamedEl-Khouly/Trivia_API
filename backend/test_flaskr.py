import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_user = os.getenv('POSTGRES_USER')
        self.database_pass = os.getenv('POSTGRES_PASSWORD')
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.database_user,self.database_pass,
            'localhost:5432', self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(type(data['categories']),dict)
        self.assertTrue(len(data['categories']))

    def test_categories_not_found(self):
        res = self.client().get('/categories')
        
        self.assertEquals(res.status_code,404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
