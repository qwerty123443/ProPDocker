import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
import re as regex
from festivalWebsite.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)

    return wrapped_view

def admin_only(view):
    """View decorator that redirects non-admin users to a 403 page.
    also redirects anonymous users to the login page

    :raise 403: if the user isn't an admin"""
    @functools.wraps(view)
    @login_required
    def wrapped_func(*args, **kwargs):
        if g.user['userType'] <= 1:
            abort(403)
        return view(*args, **kwargs)
    return wrapped_func

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session or HTTP Basic authentication is provided,
    load the user object from database into ``g.user``.
    """

    db = get_db()
    if request.authorization:
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (request.authorization['username'],)
        ).fetchone()
        if user and check_password_hash(user['password'], request.authorization['password']):
            g.user = user
        else:
            g.user = None
    else:
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = db.execute(
                'SELECT * FROM user WHERE id = ?', (user_id,)
            ).fetchone()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if g.user:
        return render_template('auth/alreadyloggedin.html.j2')
    error = []
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordconfirm = request.form['passwordconfirm']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        street = request.form['street']
        housenumber = request.form['housenumber']
        housenumberaddition = request.form['housenumberaddition']
        city = request.form['city']
        province = request.form['province']
        email = request.form['email']

        try:
            userType =  int(request.form['userType'])
        except:
            error.append('User type must be an integer.')
            userType = 0
        if not username:
            error.append('Username is required.')
        if not password:
            error.append('Password is required.')
        if password != passwordconfirm:
            error.append('Make sure both passwords are the same.')
        if  (not regex.search(r'[0-9]{1,}', password) and
                not regex.search(r'[A-Z]{1,}', password) and
                not regex.search(r'[a-z]{1,}', password) and
                not regex.search(r'.{8,}', password)):
            error.append('Password must contain at least 1 uppercase character, 1 lower case character,'+
            '1 number and must be at least 8 characters long')
        if userType <= -1:
            error.append('User type is required.')
        if not firstname:
            error.append('First name is required')
        if not lastname:
            error.append('Last name is required')
        if not birthdate:
            error.append('Birthdate is required')
        if not street:
            error.append('Street is required')
        if not housenumber:
            error.append('House number is required')
        if not city:
            error.append('City is required')
        if not province:
            error.append('Province is required')
        if not email:
            error.append('email is required')
        db = get_db()
        if db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error.append('User {0} is already registered.'.format(username))

        if error == []:
            password = generate_password_hash(password)
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                'INSERT INTO user (username, password, userType, firstname, lastname, birthdate, street, housenumber, housenumberaddition, city, province, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                  (username, password, userType, firstname, lastname, birthdate, street, housenumber, housenumberaddition, city, province, email)
            )
            db.commit()
            return redirect(url_for('auth.login'))

    for _error in error:
        flash(_error)
    if not request.form:
        request.form = {}
    return render_template('auth/register.html.j2', form=request.form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if g.user:
        return render_template('auth/alreadyloggedin.html.j2')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html.j2')

@bp.route('/accountInfo')
@login_required
def accountInfo():
    """Get account info for the signed in user."""
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (g.user['id'],)
    ).fetchone()
    return render_template('info/accountInfo.html.j2', user=user)

@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('index'))
