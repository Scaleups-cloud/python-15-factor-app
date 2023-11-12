import unittest
from app import create_app, db

class BookRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            # Create all database tables
            db.create_all()
            # Create a test user
            self.create_test_user()

    def tearDown(self):
        with self.app.app_context():
            # Drop all database tables
            db.session.remove()
            db.drop_all()

    def create_test_user(self):
        # Create a new user for testing purposes
        self.client.post('/auth/signup', json={
            'username': 'testuser',
            'password': 'testpassword'
        })

    def login_test_user(self):
        # Login the test user and get the token
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        return response.json['token']

    def test_get_books(self):
        # Login and get the token
        token = self.login_test_user()

        # Make a GET request to the books endpoint with the token
        response = self.client.get('/books/', headers={'Authorization': f'{token}'})
        self.assertEqual(response.status_code, 200)


    def test_create_book(self):
        token = self.login_test_user()
        new_book_data = {
            'title': 'New Book',
            'author': 'Author Name',
            'year_published': 2021,
            'isbn': '1234567890123'
        }
        response = self.client.post('/books/',
                                    json=new_book_data,
                                    headers={'Authorization': f'{token}'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Book added successfully', response.json['message'])

    def test_update_book(self):
        token = self.login_test_user()

        # First, create a new book
        new_book_data = {
            'title': 'Initial Title',
            'author': 'Initial Author',
            'year_published': 2021,
            'isbn': '1234567890123'
        }
        create_response = self.client.post('/books/',
                                           json=new_book_data,
                                           headers={'Authorization': f'{token}'})
        self.assertEqual(create_response.status_code, 201)

        # Get the ID of the newly created book
        new_book_id = 1

        # Now, update the book
        updated_book_data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'year_published': 2022,
            'isbn': '1234567890124'
        }
        update_response = self.client.put(f'/books/{new_book_id}',
                                          json=updated_book_data,
                                          headers={'Authorization': f'{token}'})
        self.assertEqual(update_response.status_code, 200)
        self.assertIn('Book updated successfully', update_response.json['message'])

if __name__ == '__main__':
    unittest.main()