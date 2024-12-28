from __future__ import annotations

from datetime import datetime
from datetime import timezone

from flask_login import UserMixin
from sqlalchemy.orm import Query
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from webapp.model import BaseModel
from webapp.model import db


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)


class User(BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    email = db.Column(db.String(50))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(
        db.DateTime,
        default=datetime.now(tz=timezone.utc),
    )
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic',
    )

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @property
    def is_admin(self) -> None:
        return self.role == 'admin'

    def __repr__(self) -> str:
        return f'<User {self.username}'

    def follow(self, user: User) -> None:
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user: User) -> None:
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user: User) -> bool:
        return self.followed.filter(
            followers.c.followed_id == user.id,
        ).count() > 0

    def followed_posts(self) -> Query:
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id),
        ).filter(
            followers.c.follower_id == self.id,
        ).order_by(
            Post.timestamp.desc(),
        )


class Post(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=datetime.now(tz=timezone.utc),
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
    )

    def __repr__(self) -> str:
        return f'<Post {self.body} {self.user_id}>'
