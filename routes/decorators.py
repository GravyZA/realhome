from functools import wraps
from flask import session, redirect, url_for, flash

def estate_agent_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != 'Estate Agent':
            flash('Access denied. Estate agents only.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("You need to be logged in to perform this action.")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function