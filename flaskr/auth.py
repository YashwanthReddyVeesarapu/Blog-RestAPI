from flask import Blueprint, request, jsonify

from flaskr.models import User
from flaskr.config.tokens import generate_token, decode_token
from flaskr.config.utils import hash_password, check_password

# Create a Blueprint for the authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Route for user signup
@auth_bp.route('/signup', methods=['POST'])
def signup():
    # Get email and password from request
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Check if email and password are provided
    if not email or not password:
        return jsonify({'error': 'Missing username, email or password'}), 400
    
    # Check if email is already in use
    if User.get_by_email(email):
        return jsonify({'error': 'Email already in use'}), 400
    
    # Hash the password
    password = hash_password(password)
    
    # Create a new user and save to database
    user = User(email=email, password=password)
    user.save()
    
    return jsonify({'message': 'User created successfully'}), 201

# Route for user login
@auth_bp.route('/login', methods=['POST'])
def login():
    # Get email and password from request
    email = request.json.get('email')
    password = request.json.get('password')
    
    # Find user by email
    user = User.get_by_email(email)
    
    # Check if user exists and password is correct
    if not user or not check_password(password, user['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Generate token for authentication
    token = generate_token(user['_id'])

    return jsonify({'message': 'Login successful', 'token': token, 'uid': user['_id']}), 200

# Route to verify authentication token
@auth_bp.route('/verify', methods=['GET'])
def verify():
    # Get token from request headers
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    
    try:
        # Decode token and get user ID
        data = decode_token(token)
        user = User.get_by_id(data['uid'])
        
        # Check if user exists
        if not user:
            return jsonify({'error': 'Invalid token'}), 401
        
        # Generate new token (refresh token)
        new_token = generate_token(user['_id'])
        return jsonify({'message': 'Token is valid', 'uid': user['_id'], 'token': new_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for user logout (for testing purposes)
@auth_bp.route('/logout', methods=['GET'])
def logout():
    return jsonify({'message': 'Logout successful'}), 200
