from sqlalchemy.orm import backref

from app.extensions import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    body = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    active = db.Column(db.Boolean)