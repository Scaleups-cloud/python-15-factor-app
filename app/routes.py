from flask_restx import Namespace, Resource, fields
from .models import db, Book

api = Namespace('books', description='Books operations')

book_model = api.model('Book', {
    'id': fields.Integer(readOnly=True, description='The book unique identifier'),
    'title': fields.String(required=True, description='The book title'),
    'author': fields.String(required=True, description='The book author'),
    'year_published': fields.Integer(description='The year the book was published'),
    'isbn': fields.String(required=True, description='The ISBN of the book')
})

@api.route('/')
class BookList(Resource):
    @api.marshal_list_with(book_model)
    def get(self):
        """List all books"""
        books = Book.query.all()
        return books

    @api.expect(book_model)
    def post(self):
        """Create a new book"""
        data = api.payload
        new_book = Book(title=data['title'], author=data['author'],
                        year_published=data.get('year_published'), isbn=data['isbn'])
        db.session.add(new_book)
        db.session.commit()
        return {'message': 'Book added successfully'}, 201

@api.route('/<int:id>')
@api.response(404, 'Book not found')
class BookItem(Resource):
    @api.marshal_with(book_model)
    def get(self, id):
        """Fetch a book given its identifier"""
        book = Book.query.get_or_404(id)
        return book

    @api.expect(book_model)
    def put(self, id):
        """Update a book given its identifier"""
        book = Book.query.get_or_404(id)
        data = api.payload
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.year_published = data.get('year_published', book.year_published)
        book.isbn = data.get('isbn', book.isbn)
        db.session.commit()
        return {'message': 'Book updated successfully'}

    def delete(self, id):
        """Delete a book given its identifier"""
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}