from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()

class User(db.Model):
    """Model for the users table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class TokenBlacklist(db.Model):
    """Model for the token_blacklist table"""
    __tablename__ = 'token_blacklist'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, token):
        self.token = token

class Book(db.Model):
    """Model for the books table"""
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    year_published = db.Column(db.Integer)
    isbn = db.Column(db.String(13), unique=True, nullable=False)

    def __init__(self, title, author, year_published, isbn):
        self.title = title
        self.author = author
        self.year_published = year_published
        self.isbn = isbn

    def __repr__(self):
        return f'<Book {self.title}>'
