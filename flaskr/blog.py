from flask import Blueprint, request, jsonify

from flaskr.models import Post
from flaskr.config.auth_wrap import token_required

# Create a Blueprint for the blog routes
blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

# Route for creating a new post
@blog_bp.route('/posts', methods=['POST'])
@token_required
def create_post(current_user):
    # Get data from request
    data = request.json
    author_id = data.get('author_id')
    title = data.get('title')
    content = data.get('content')
    description = data.get('description')

    # Check if request is JSON
    if not request.is_json:
        return jsonify({'error': 'Missing request body'}), 400

    # Check if author_id matches current user's ID
    if author_id != current_user['_id']:
        return jsonify({'error': 'Unauthorized'}), 401

    # Check for missing required fields
    if not (title and content and description and author_id):
        return jsonify({'error': 'Missing required fields'}), 400

    # Create and save the post
    post = Post(title=title, content=content, description=description, author_id=author_id)
    post_id = post.save()

    return jsonify({'message': 'Post created successfully', 'post_id': post_id}), 201

# Route for getting all posts
@blog_bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.get_all()
    return jsonify(posts), 200

# Route for getting a specific post
@blog_bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post), 200

# Route for updating a post
@blog_bp.route('/posts/<post_id>', methods=['PUT'])
@token_required
def update_post(current_user, post_id):
    # Get data from request
    data = request.json
    title = data.get('title')
    content = data.get('content')
    description = data.get('description')

    # Check if request is JSON
    if not request.is_json:
        return jsonify({'error': 'Missing request body'}), 400

    # Check if post exists
    existing_post = Post.get_by_id(post_id)
    if not existing_post:
        return jsonify({'error': 'Post not found'}), 404

    # Check if user is authorized to update the post
    if existing_post['author_id'] != current_user['_id']:
        return jsonify({'error': 'Unauthorized'}), 401

    # Check for missing required fields
    if not (title and content and description):
        return jsonify({'error': 'Missing required fields'}), 400

    # Update the post
    post = Post.update(post_id, title, content, description)
    if not post:
        return jsonify({'error': 'Unable to update post'}), 500

    return jsonify({'message': 'Post updated successfully'}), 200

# Route for deleting a post
@blog_bp.route('/posts/<post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    # Check if post exists
    existing_post = Post.get_by_id(post_id)
    if not existing_post:
        return jsonify({'error': 'Post not found'}), 404
    
    # Check if user is authorized to delete the post
    if existing_post['author_id'] != current_user['_id']:
        return jsonify({'error': 'Unauthorized'}), 401

    # Delete the post
    post = Post.delete(post_id)
    if not post:
        return jsonify({'error': 'Unable to delete post'}), 500
    return jsonify({'message': 'Post deleted successfully'}), 200