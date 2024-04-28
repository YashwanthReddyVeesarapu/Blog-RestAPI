# Flask Blog API

This is a simple RESTful API built using Flask for managing blog posts.

## Features

- User authentication (signup, login, logout)
- CRUD operations for blog posts (create, read, update, delete)
- Token-based authentication using JWT

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/flask-blog-api.git
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MongoDB:**

   - Install MongoDB on your system if you haven't already.
   - Create a MongoDB database named 'blog'.
   - Update the MongoDB URI in the .env

4. **Set up environment variables:**

   - Create a `.env` file in the root directory.
   - Add the following environment variables to the `.env` file:

     ```env
     SECRET=your_secret_key
     MONGO_URI=your_mongodb_uri
     ```

## Usage

1. **Run the Flask application:**

   ```bash
   flask run --app=flaskr --debug
   ```

2. **Access the API endpoints using a tool like cURL, Postman, or any REST client.**

## Endpoints

### Authentication

- `POST /auth/signup`: Create a new user account.
- `POST /auth/login`: Log in with an existing user account.
- `GET /auth/verify`: Verify the authentication token.
- `GET /auth/logout`: Log out the user (for testing purposes).

### Blog Posts

- `POST /blog/posts`: Create a new blog post.
- `GET /blog/posts`: Get all blog posts.
- `GET /blog/posts/<post_id>`: Get a specific blog post.
- `PUT /blog/posts/<post_id>`: Update a blog post.
- `DELETE /blog/posts/<post_id>`: Delete a blog post.

## Testing

To run tests, execute the following command:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

To test the API endpoints, you can use the Postman collection provided in the repository.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
