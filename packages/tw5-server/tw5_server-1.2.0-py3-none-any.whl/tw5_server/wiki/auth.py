from functools import wraps
from flask import abort, request
from tw5_server import settings


def get_basic_auth_password():
    authorization = request.authorization or {}
    return authorization.get('password', '')


def get_key(wiki_name, key_type, default=None):
    authorization = settings.CONFIG.get('TW5_AUTHENTICATION', {})
    authorization = authorization.get(wiki_name, {})
    return authorization.get(key_type, default)


def can_view(wiki_name, password):
    view_key = get_key(wiki_name, 'view_key', settings.DEFUALT_VIEW_KEY)
    write_key = get_key(wiki_name, 'write_key', settings.DEFAULT_WRITE_KEY)
    return password in (view_key, write_key)


def can_write(wiki_name, password):
    write_key = get_key(wiki_name, 'write_key', settings.DEFAULT_WRITE_KEY)
    return password == write_key


def view_permission_required(f):
    @wraps(f)
    def decorated_function(*args, wiki_name='', **kwargs):
        password = get_basic_auth_password()
        if not can_view(wiki_name, password):
            abort(401)
        return f(*args, wiki_name=wiki_name, **kwargs)

    return decorated_function


def write_permission_required(f):
    @wraps(f)
    def decorated_function(*args, wiki_name='', **kwargs):
        password = get_basic_auth_password()
        if not can_write(wiki_name, password):
            abort(401)
        return f(*args, wiki_name=wiki_name, **kwargs)

    return decorated_function
