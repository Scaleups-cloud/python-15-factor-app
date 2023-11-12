import unittest
from app import create_app, db
from app.models import Book

class TestBookModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_book_creation(self):
        book = Book(title='Test Book', author='Test Author', year_published=2020, isbn='1234567890123')
        db.session.add(book)
        db.session.commit()

        # Verify the book is added to the database
        added_book = Book.query.filter_by(isbn='1234567890123').first()
        self.assertIsNotNone(added_book)
        self.assertEqual(added_book.title, 'Test Book')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    if __name__ == '__main__':
        unittest.main()