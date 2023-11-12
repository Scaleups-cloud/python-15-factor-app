import datetime
import jwt
from flask import current_app, request, jsonify
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import db, User, TokenBlacklist
from ..utils.auth_decorators import token_required, admin_required, blacklist_token
from ..utils.app_logger import setup_logger

logger = setup_logger(__name__)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter your bearer token in the format: Bearer <token>'
    }
}
ns_auth = Namespace('auth', description='Authentication operations', authorizations=authorizations, security='Bearer Auth')

# Define models for Swagger
signup_model = ns_auth.model('Signup', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

login_model = ns_auth.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

token_model = ns_auth.model('Token', {
    'token': fields.String(description='JWT Token'),
})

def generate_token(user):
    """
    Generates the Auth Token for a given user.
    """
    try:
        # Set the payload with an expiration time and user identifier
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': user.id
        }

        # Create the JWT token
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        logger.error("Token generation failed", extra={"error": str(e)})
        return e

@ns_auth.route('/signup')
class SignupUser(Resource):
    @ns_auth.expect(signup_model)
    @ns_auth.marshal_with(token_model, code=201)
    def post(self):
        """Register a new user"""
        try:
            data = ns_auth.payload
            hashed_password = generate_password_hash(data['password'], method='sha256')
            new_user = User(username=data['username'], password=hashed_password, is_admin=False)
            db.session.add(new_user)
            db.session.commit()

            logger.info("New user registered", extra={"username": data['username']})
            return {'token': generate_token(new_user)}, 201

        except Exception as e:
            logger.error("Signup failed", extra={"error": str(e)})
            raise e

@ns_auth.route('/login')
class LoginUser(Resource):
    @ns_auth.doc(security='Bearer Auth')
    @ns_auth.expect(login_model)
    @ns_auth.marshal_with(token_model, code=200)
    def post(self):
        """Authenticate a user and return a token"""
        try:
            data = ns_auth.payload
            user = User.query.filter_by(username=data['username']).first()
            if not user or not check_password_hash(user.password, data['password']):
                logger.warning("Invalid login attempt", extra={"username": data['username']})
                return {'message': 'Invalid username or password!'}, 401

            token = generate_token(user)
            logger.info("User logged in", extra={"username": data['username']})
            return {'token': token}, 200

        except Exception as e:
            logger.error("Login failed", extra={"error": str(e)})
            raise e

@ns_auth.route('/logout')
class LogoutUser(Resource):
    @token_required
    def post(self):
        """Logout a user by blacklisting their token"""
        try:
            token = request.headers.get('Authorization')
            if not token:
                logger.warning("Logout attempt without token")
                return {'message': 'Token is missing!'}, 403

            success, message = blacklist_token(token)
            if success:
                logger.info("User logged out", extra={"token": token})
                return {'message': message}, 200
            else:
                logger.warning("Logout failed", extra={"message": message})
                return {'message': message}, 400
        except Exception as e:
            logger.error("Logout error", extra={"error": str(e)})
            return {'message': str(e)}, 500
