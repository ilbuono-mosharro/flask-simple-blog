from sqlalchemy.orm import relationship

from app.extensions import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    comments = relationship('Comment', backref='comment', lazy=True)
    posts = relationship('Blog', backref='blog', lazy=True)