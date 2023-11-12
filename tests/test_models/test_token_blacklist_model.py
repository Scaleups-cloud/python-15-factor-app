import unittest
from app import create_app, db
from app.models import TokenBlacklist

class TestTokenBlacklistModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_token_blacklisting(self):
        token = 'testtoken'
        blacklisted_token = TokenBlacklist(token=token)
        db.session.add(blacklisted_token)
        db.session.commit()

        # Verify the token is blacklisted
        found_token = TokenBlacklist.query.filter_by(token=token).first()
        self.assertIsNotNone(found_token)
        self.assertEqual(found_token.token, token)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()