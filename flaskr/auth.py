from flask import Blueprint, request, jsonify

from flaskr.models import User

from flaskr.config.tokens import generate_token, decode_token

from flaskr.config.utils import hash_password, check_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not password:
        return jsonify({'error': 'Missing username, email or password'}), 400
    if User.get_by_email(email):
        return jsonify({'error': 'Email already in use'}), 400
    password = hash_password(password)
    user = User(email=email, password=password)
    user.save()
    return jsonify({'message': 'User created successfully'}), 201



@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.get_by_email(email)
    if not user or not check_password(password, user['password'] ):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Generate token
    token = generate_token(user['_id'])

    return jsonify({'message': 'Login successful', 'token': token, 'uid': user['_id'] }), 200


# verify token
@auth_bp.route('/verify', methods=['GET'])
def verify():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is missing'}), 401
    try:
        data = decode_token(token)
        user = User.get_by_id(data['uid'])
        if not user:
            return jsonify({'error': 'Invalid token'}), 401
        
        new_token = generate_token(user['_id'])
        return jsonify({'message': 'Token is valid', 'uid': user['_id'], 'token': new_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    



# Testing purposes
@auth_bp.route('/logout', methods=['GET'])
def logout():
    return jsonify({'message': 'Logout successful'}), 200