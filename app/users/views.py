import functools

from flask import render_template, request, redirect, session, url_for, flash, g
from werkzeug.security import generate_password_hash, check_password_hash

from . import bp
from app.extensions import db
from .models import User


@bp.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=generate_password_hash(request.form['password']),
            email=request.form["email"],
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("users.login"))

    return render_template("auth/register.html")


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.one_or_404(
            db.select(User).filter_by(username=username),
            description=f"No user named '{username}'."
        )

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('blog.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_or_404(User, user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('users.login'))

        return view(**kwargs)

    return wrapped_view
