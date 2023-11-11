from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from .routes import api as books_ns
from .models import db
from config import config_by_name

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)

    # Setup Flask-RESTx
    api = Api(app, version='1.0', title='Book API', description='A simple Book API')
    api.add_namespace(books_ns, path='/api/books')

    return app
