from functools import wraps
from flask import request, abort
from flaskr.models import User
from flaskr.config.tokens import decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get token from request headers
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        
        # Check if token is missing
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        
        try:
            # Decode token and get user data
            data = decode_token(token)
            current_user = User.get_by_id(data["uid"])
            
            # Check if user exists
            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            
            # Check if user ID in token matches user ID in database
            if current_user["_id"] != data["uid"]:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            
        except Exception as e:
            # Handle any exceptions
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
        
        # Call the decorated function with current user as argument
        return f(current_user, *args, **kwargs)

    return decorated
