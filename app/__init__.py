from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_by_name
from .models import db
from .routes import bp
from .utils.database import init_db

def create_app(config_name):
    app = Flask(__name__)

    # Load configuration from the 'config' module
    app.config.from_object(config_by_name[config_name])

    # Initialize and bind SQLAlchemy to the app
    db.init_app(app)

    # Register the Blueprint for routes
    app.register_blueprint(bp)

    return app
