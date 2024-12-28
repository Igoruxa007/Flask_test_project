from __future__ import annotations

from webapp.model import BaseModel
from webapp.model import db


class News(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f'<News {self.title} {self.url}>'
