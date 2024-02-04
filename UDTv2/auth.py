import functools
from werkzeug.security import check_password_hash, generate_password_hash
from UDTv2.models import Users, db
from sqlalchemy import select

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


authBP = Blueprint('auth', __name__, url_prefix='/auth')

@authBP.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        firstname = request.form['first-name']
        lastname = request.form['last-name']
        email = request.form['email']
        password = request.form['password']
        error = None

        if not email:
            error = 'Invalid: email is required'
        elif not password:
            error = 'Invalid: password is required'

        if error is None:
            try:
                user = Users(name=f"{firstname.capitalize()} {lastname.capitalize()}", email=email, password=password)
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                print(f"Error: {e}")
                db.session.rollback()
                return redirect(url_for('auth.register'))
            finally:
                return redirect(url_for('auth.login'))
                   

    return render_template('auth/register.html')


@authBP.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        user = Users.query.filter_by(email=email).first()

        if user is None:
            error = 'Incorrect email'
        elif not user.verify_password(password):
            error = 'Incorrect Password'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')


@authBP.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.filter_by(id=user_id).first()


@authBP.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view