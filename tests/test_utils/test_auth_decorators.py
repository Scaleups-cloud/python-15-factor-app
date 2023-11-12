import unittest
from app import create_app, db
from app.models import User, TokenBlacklist
from app.utils.auth_decorators import token_required, admin_required, decode_token, blacklist_token, is_token_blacklisted
from unittest.mock import patch
from flask import jsonify

class TestAuthDecorators(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.create_test_user()

    def create_test_user(self):
        new_user = User(username='testuser', password='hashed_password', is_admin=False)
        db.session.add(new_user)
        db.session.commit()

    def login_test_user(self):
        # Simulate login to get a token. Adjust as per your application's implementation
        return 'test_token'

    def test_decode_token(self):
        with self.app.app_context():
            with patch('jwt.decode', return_value={'sub': 1}):
                user = decode_token('fake_token')
                self.assertIsNotNone(user)

    def test_token_required_decorator(self):
        @token_required
        def mock_route():
            return jsonify(success=True), 200

        with self.app.test_request_context('/', headers={'Authorization': 'Bearer fake_token'}):
            with self.app.app_context():
                with patch('app.utils.auth_decorators.decode_token', return_value=User.query.first()):
                    response, status_code = mock_route()
                    self.assertEqual(status_code, 200)

    def test_admin_required_decorator(self):
        @admin_required
        def mock_route():
            return jsonify(success=True), 200

        with self.app.test_request_context('/', headers={'Authorization': 'Bearer fake_admin_token'}):
            with self.app.app_context():
                # Mock a user with is_admin set to True
                with patch('app.utils.auth_decorators.decode_token',
                           return_value=User(username='admin', password='hashed_password', is_admin=True)):
                    response, status_code = mock_route()
                    self.assertEqual(status_code, 200)

    def test_blacklist_token(self):
        with self.app.app_context():
            token = 'new_token'
            blacklist_token(token)
            self.assertTrue(is_token_blacklisted(token))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()