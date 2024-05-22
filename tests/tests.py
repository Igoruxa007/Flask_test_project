from datetime import datetime, timezone, timedelta
import os
import unittest

from webapp import create_app, db
from webapp.user.models import User, Post

os.environ['DATABASE_URL'] = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = create_app().app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan', email='test@m.ru')
        u.set_password('dog')
        self.assertFalse(u.check_password('cat'))
        self.assertTrue(u.check_password('dog'))

    def test_follow(self):
        u1 = User(username='John', email='j@j.j')
        u2 = User(username='Hohn', email='h@h.h')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.username, 'John')
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        u1 = User(username='John', email='j@j.j')
        u2 = User(username='Hohn', email='h@h.h')
        u3 = User(username='Aohn', email='a@a.a')
        u4 = User(username='Bohn', email='b@b.b')
        db.session.add_all([u1, u2, u3, u4])

        now = datetime.now(tz=timezone.utc)
        p1 = Post(body="post 1", user_id=u1.id,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post 2", user_id=u2.id,
                  timestamp=now + timedelta(seconds=2))
        p3 = Post(body="post 3", user_id=u3.id,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post 4", user_id=u4.id,
                  timestamp=now + timedelta(seconds=4))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2)
        u1.follow(u3)
        u2.follow(u3)
        u3.follow(u4)
        db.session.commit()

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p3])
        self.assertEqual(f2, [p3])
        self.assertEqual(f3, [p4])
        self.assertEqual(f4, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
