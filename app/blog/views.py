import datetime

from flask import (
    flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.extensions import db
from . import bp
from .models import Blog
from ..users.views import login_required
from app.comment.models import Comment

@bp.route('/')
def index():
    posts = db.session.execute(db.select(Blog).order_by(Blog.title)).scalars()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            blog = Blog(title=title, body=body, author_id=g.user.id, slug=title, created=datetime.datetime.now())
            db.session.add(blog)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/detail', methods=('GET', 'POST'))
def detail(id):
    post = db.get_or_404(Blog, id)
    if request.method == "POST":
        body = request.form['body']
        comment = Comment(author_id=g.user.id, post_id=post.id, body=body, created=datetime.datetime.now(),
                         updated=datetime.datetime.now(), active=True)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blog.detail', id=post.id))

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return render_template('blog/detail.html', post=post)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = db.one_or_404(db.select(Blog).filter_by(id=id, author_id=g.user.id))

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = db.one_or_404(db.select(Blog).filter_by(id=id, author_id=g.user.id))
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('blog.index'))