from flask_restx import Namespace, Resource, fields
from ..models import db, User, Book
from ..utils.auth_decorators import token_required, admin_required

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter your bearer token in the format: Bearer <token>'
    }
}
ns_books = Namespace('books', description='Books operations', authorizations=authorizations, security='Bearer Auth')

book_model = ns_books.model('Book', {
    'id': fields.Integer(readOnly=True, description='The book unique identifier'),
    'title': fields.String(required=True, description='The book title'),
    'author': fields.String(required=True, description='The book author'),
    'year_published': fields.Integer(description='The year the book was published'),
    'isbn': fields.String(required=True, description='The ISBN of the book')
})

@ns_books.route('/')
class BookList(Resource):
    @ns_books.doc(security='Bearer Auth')
    @ns_books.marshal_list_with(book_model)
    @token_required
    def get(self):
        """List all books"""
        books = Book.query.all()
        return books

    @ns_books.expect(book_model)
    @token_required
    def post(self):
        """Create a new book"""
        data = ns_books.payload
        new_book = Book(title=data['title'], author=data['author'],
                        year_published=data.get('year_published'), isbn=data['isbn'])
        db.session.add(new_book)
        db.session.commit()
        return {'message': 'Book added successfully'}, 201

@ns_books.route('/<int:id>')
@ns_books.response(404, 'Book not found')
class BookItem(Resource):
    @ns_books.marshal_with(book_model)
    @token_required
    def get(self, id):
        """Fetch a book given its identifier"""
        book = Book.query.get_or_404(id)
        return book

    @ns_books.expect(book_model)
    @token_required
    def put(self, id):
        """Update a book given its identifier"""
        book = Book.query.get_or_404(id)
        data = ns_books.payload
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.year_published = data.get('year_published', book.year_published)
        book.isbn = data.get('isbn', book.isbn)
        db.session.commit()
        return {'message': 'Book updated successfully'}

    @token_required
    @admin_required
    def delete(self, id):
        """Delete a book given its identifier"""
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}
