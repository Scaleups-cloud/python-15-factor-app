from flask import Flask
from flask_restx import Api
from .models import db
from .routes.auth_routes import ns_auth
from .routes.book_routes import ns_books
from config import config_by_name

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Enter your bearer token in the format: Bearer <token>'
        }
    }

    api = Api(app, authorizations=authorizations, security='Bearer Auth', version='1.0', title='My API', description='A simple API')
    api.add_namespace(ns_auth)
    api.add_namespace(ns_books)

    return app
