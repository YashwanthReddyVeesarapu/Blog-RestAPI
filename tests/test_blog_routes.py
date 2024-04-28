import unittest
from flask import Flask
from flaskr.blog import blog_bp

class TestFlaskAPI(unittest.TestCase):

    def setUp(self):
        # Create a test Flask app and register the blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(blog_bp)
        self.client = self.app.test_client()
        self.app.config["MONGO_URI"] = "mongodb://localhost:27017/blog"
        
        # Add test data
        self.post_id = self.add_test_post()

    def tearDown(self):
        # Clean up test data
        self.delete_test_post()

    def add_test_post(self):
        # Add a test post and return its ID
        data = {
            "title": "Test Post",
            "content": "This is a test post",
            "description": "Testing post creation",
            "author_id": "123456"
        }
        response = self.client.post('/blog/posts', json=data)
        post_data = response.json 
        return post_data.get('post_id')

    def delete_test_post(self):
        # Delete the test post
        if self.post_id:
            self.client.delete(f'/blog/posts/{self.post_id}')

    def test_create_post(self):
        # Test creating a new post
        data = {
            "title": "Test Post",
            "content": "This is a test post",
            "description": "Testing post creation",
            "author_id": "123456"
        }
        response = self.client.post('/blog/posts', json=data)
        self.assertEqual(response.status_code, 201)
        # Assert that the returned JSON contains the expected keys
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'Post created successfully')

    def test_get_all_posts(self):
        # Test getting all posts
        response = self.client.get('/blog/posts')
        self.assertEqual(response.status_code, 200)
        # Assert that the returned JSON contains a list of posts
        self.assertIsInstance(response.json, list)

    def test_get_post(self):
        # Test getting a specific post
        response = self.client.get(f'/blog/posts/{self.post_id}')
        self.assertEqual(response.status_code, 200)
        # Assert that the returned JSON contains the expected keys
        self.assertIn('post', response.json)

    def test_update_post(self):
        # Test updating a post
        data = {
            "title": "Updated Title",
            "content": "Updated content",
            "description": "Updated description"
        }
        response = self.client.put(f'/blog/posts/{self.post_id}', json=data)
        self.assertEqual(response.status_code, 200)
        # Assert that the returned JSON contains the expected keys
        self.assertIn('message', response.json)
        self.assertEqual(response.json()['message'], 'Post updated successfully')

    def test_delete_post(self):
        # Test deleting a post
        response = self.client.delete(f'/blog/posts/{self.post_id}')
        self.assertEqual(response.status_code, 200)
        # Assert that the returned JSON contains the expected keys
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'Post deleted successfully')

if __name__ == '__main__':
    unittest.main()