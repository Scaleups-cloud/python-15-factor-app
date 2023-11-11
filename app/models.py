from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()

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
