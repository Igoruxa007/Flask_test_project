import os

import unittest

from webapp import create_app, db
from webapp.user.models import User

os.environ['DATABASE_URL'] = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = create_app().app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan', email='test@m.ru')
        u.set_password('dog')
        self.assertFalse(u.check_password('cat'))
        self.assertTrue(u.check_password('dog'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
