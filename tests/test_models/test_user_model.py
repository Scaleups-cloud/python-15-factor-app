import unittest
from app import create_app, db
from app.models import User

class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_user_creation(self):
        user = User(username='testuser', password='testpassword', is_admin=False)
        db.session.add(user)
        db.session.commit()

        # Test if the user is correctly added to the database
        added_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(added_user)
        self.assertEqual(added_user.username, 'testuser')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()