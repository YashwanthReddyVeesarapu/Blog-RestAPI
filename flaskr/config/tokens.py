import jwt
import os
from datetime import datetime, timedelta


SECRET = os.getenv('SECRET')

def generate_token(user_id):
    # Expiry time is set to 14 days 
    expiry = datetime.now() + timedelta(days=14)

    token = jwt.encode({
        'uid': user_id,
        'exp': expiry
    }, SECRET, algorithm='HS256')

    return token

def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=['HS256'])