import re
from functools import wraps
from random import choice
from string import ascii_uppercase, digits

import rethinkdb as r
from flask import Response, request, g, abort

from .config import config


def generate_token():
    token = None
    while token is None or r.table('tokens').filter({'id': token}).count().run(g.rdb_conn):
            token = "%08d%s" % (config.serverid, "".join(choice(ascii_uppercase + digits) for _ in range(127-8)))
    return token


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def check_auth(username, password):
    return config.auth.username == username and config.auth.password == password


def check_token(token):
    return r.table('tokens').filter({'id': token}).count().run(g.rdb_conn)


def requires_token(f=None):
    if f is None:
        return requires_token

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('authorization', None)
        if auth is None:
            abort(401)
        if not check_token(auth):
            abort(401)
        g.token = auth
        return f(*args, **kwargs)

    return decorated


def requires_auth(f=None):
    if f is None:
        return requires_auth

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


# noinspection RegExpRedundantEscape
VARIABLE_REGEX = re.compile(r"\{([a-zA-Z0-9_\-]+)\}")


def variables(text):
    return [match.group(1) for match in VARIABLE_REGEX.finditer(text)]
