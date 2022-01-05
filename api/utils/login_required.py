
from functools import wraps, update_wrapper
from flask import session, redirect,url_for

def login_required(func):
    # @wraps(func)
    def nei(*args, **kwargs):
        if session.get("username"):
            ret = func(*args, **kwargs)
            return ret
        else:
            return redirect(url_for('login'))
    update_wrapper(nei, func)
    return nei

