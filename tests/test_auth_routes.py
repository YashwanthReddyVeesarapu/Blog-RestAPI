import unittest
import json
from flask import Flask
from flaskr.auth import auth_bp  # Assuming the authentication blueprint is named auth_bp
from flaskr.models import User

class TestAuthRoutes(unittest.TestCase):

    def setUp(self):
        # Create a test Flask app and register the authentication blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(auth_bp)
        self.client = self.app.test_client()
        self.app.config["MONGO_URI"] = "mongodb://localhost:27017/blog"

    def tearDown(self):
        pass

    def test_signup(self):
        # Test user signup
        data = {
            "email": "test1@example.com",
            "password": "password123"
        }
        response = self.client.post('/auth/signup', json=data)
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        # Test user login
        data = {
            "email": "test@example.com",
            "password": "password123"
        }
        response = self.client.post('/auth/login', json=data)
        self.assertEqual(response.status_code, 200)
        # Assert that the response contains the expected keys
        self.assertIn('token', response.json)
        self.assertIn('uid', response.json)

    def test_verify(self):
        # Test token verification
        # First, sign up a user to get a valid token for testing
        signup_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        self.client.post('/auth/signup', json=signup_data)

        # Then, log in to get a token
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        login_response = self.client.post('/auth/login', json=login_data)
        token = login_response.json['token']

        # Now, verify the token
        headers = {'Authorization': token}
        response = self.client.get('/auth/verify', headers=headers)
        self.assertEqual(response.status_code, 200)
        # Assert that the response contains the expected keys
        self.assertIn('token', response.json)
        self.assertIn('uid', response.json)

    def test_logout(self):
        # Test user logout (for testing purposes)
        response = self.client.get('/auth/logout')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()