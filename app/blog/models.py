import enum
from sqlalchemy.orm import backref, relationship

from app.extensions import db



class StatusEnum(enum.IntEnum):
    draft = 1
    published = 2


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False)
    status = db.Column(
        db.Enum(StatusEnum),
        default=StatusEnum.draft,
        nullable=False
    )
    created = db.Column(db.DateTime)
    comments = relationship('Comment', backref='post', lazy=True)
