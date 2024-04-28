from flask import Blueprint, request, jsonify

from flaskr.models import Post
from flaskr.config.auth_wrap import token_required


blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

@blog_bp.route('/posts', methods=['POST'])
@token_required
def create_post(current_user):
    author_id = request.json.get('author_id')
    if not request.is_json:
        return jsonify({'error': 'Missing request body'}), 400
    if author_id != current_user['_id']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    title = request.json.get('title')
    content = request.json.get('content')
    description = request.json.get('description')
    author_id = request.json.get('author_id')

    if not title or not content or not description or not author_id:
        return jsonify({'error': 'Missing required fields'}), 400
    post = Post(title=title, content=content, description=description, author_id=author_id)
    post_id = post.save()

    return jsonify({'message': 'Post created successfully', 
        'post_id': post_id
    }), 201

@blog_bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.get_all()
    return posts, 200

@blog_bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post), 200

@blog_bp.route('/posts/<post_id>', methods=['PUT'])
@token_required
def update_post(current_user, post_id):
    print(post_id)
    if not request.is_json:
        return jsonify({'error': 'Missing request body'}), 400
    
    existing_post = Post.get_by_id(post_id)
    if not existing_post:
        return jsonify({'error': 'Post not found'}), 404
        
    if existing_post['author_id'] != current_user['_id']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    title = request.json.get('title')
    content = request.json.get('content')
    description = request.json.get('description')
    
    if not title or not content or not description:
        return jsonify({'error': 'Missing required fields'}), 400
    post = Post.update(post_id, title, content, description)
    if not post:
        return jsonify({'error': 'Unable to update post'}), 500
    
    return jsonify({'message': 'Post updated successfully'}), 200

@blog_bp.route('/posts/<post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    existing_post = Post.get_by_id(post_id)
    if not existing_post:
        return jsonify({'error': 'Post not found'}), 404
    
    if existing_post['author_id'] != current_user['_id']:
        return jsonify({'error': 'Unauthorized'}), 401

    post = Post.delete(post_id)
    if not post:
        return jsonify({'error': 'Unable to delete post'}), 500
    return jsonify({'message': 'Post deleted successfully'}), 200


