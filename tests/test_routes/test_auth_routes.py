import unittest
from app import create_app, db

class AuthRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup_user(self):
        response = self.client.post('/auth/signup', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.json)

    def test_login_user(self):
        # First, create a user to login
        self.client.post('/auth/signup', json={
            'username': 'loginuser',
            'password': 'loginpassword'
        })

        # Attempt to login with the created user
        response = self.client.post('/auth/login', json={
            'username': 'loginuser',
            'password': 'loginpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_logout_user(self):
        # First, create and login a user to get a token
        self.client.post('/auth/signup', json={
            'username': 'logoutuser',
            'password': 'logoutpassword'
        })
        login_response = self.client.post('/auth/login', json={
            'username': 'logoutuser',
            'password': 'logoutpassword'
        })
        token = login_response.json['token']

        # Attempt to logout with the token
        response = self.client.post('/auth/logout',
                                    headers={'Authorization': f'{token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

if __name__ == '__main__':
    unittest.main()