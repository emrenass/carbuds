from functools import wraps
from flask import Flask, make_response, request, redirect
from flask import current_app as app
import jwt


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')

        if not token:
            return make_response(redirect('/login'))
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return make_response(redirect('/login'))

        return f(*args, **kwargs)

    return decorated
