from flask import Flask

from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    #
    # from app.users.models import User
    # from app.blog.models import Blog
    # from app.comment.models import Comment
    # with app.app_context():
    #     # db.drop_all()
    #     db.create_all()

    # Register blueprints here
    from app.users.views import bp as users_bp
    app.register_blueprint(users_bp)
    from app.blog.views import bp as blog_bp
    app.register_blueprint(blog_bp)

    return app