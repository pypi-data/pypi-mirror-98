from flask import Blueprint, redirect, url_for, flash, render_template, jsonify, request, session, g
from app.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        

    return render_template('login.html')