import jwt
from functools import wraps
from flask import request, jsonify, current_app
from ..models import User, TokenBlacklist

def decode_token(token):
    """
    Decodes the auth token and returns the user object.
    """
    try:
        # Decode the token with the secret key
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=["HS256"])
        return User.query.get(payload['sub'])  # Assuming 'sub' contains the user ID
    except jwt.ExpiredSignatureError:
        raise Exception('Token expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token. Please log in again.')

def is_token_blacklisted(token):
    # Check if the token is in the blacklist
    return TokenBlacklist.query.filter_by(token=token).first() is not None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        print("token is: ")
        print(token)

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        if is_token_blacklisted(token):
            return jsonify({'message': 'Token has been blacklisted'}), 403

        try:
            user_id = decode_token(token)
            if isinstance(user_id, str):  # Error message returned
                return jsonify({'message': user_id}), 403
        except:
            return jsonify({'message': 'Invalid or expired token!'}), 403

        return f(*args, **kwargs)
    return decorated

# Admin role verification decorator
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        if is_token_blacklisted(token):
            return jsonify({'message': 'Token has been blacklisted'}), 403

        try:
            user = decode_token(token)
            if not user.is_admin:
                raise Exception('Not an admin')
        except:
            return jsonify({'message': 'Unauthorized access or invalid token!'}), 403

        return f(*args, **kwargs)
    return decorated

from ..models import db, TokenBlacklist

def blacklist_token(token):
    """
    Adds the given token to the blacklist.
    """
    if not token:
        return None, "No token provided."

    if is_token_blacklisted(token):
        return False, "Token is already blacklisted."

    try:
        new_blacklist_token = TokenBlacklist(token=token)
        db.session.add(new_blacklist_token)
        db.session.commit()
        return True, "Token has been blacklisted successfully."
    except Exception as e:
        return None, str(e)
