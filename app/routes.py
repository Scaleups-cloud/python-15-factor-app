from flask import request, jsonify, Blueprint
from .models import db, Book
from flask import abort

bp = Blueprint('bp', __name__, url_prefix='/api')

@bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        year_published=data.get('year_published'),
        isbn=data['isbn']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

@bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'year_published': book.year_published,
        'isbn': book.isbn
    } for book in books])

@bp.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'year_published': book.year_published,
        'isbn': book.isbn
    })

@bp.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.year_published = data.get('year_published', book.year_published)
    book.isbn = data.get('isbn', book.isbn)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

@bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})
