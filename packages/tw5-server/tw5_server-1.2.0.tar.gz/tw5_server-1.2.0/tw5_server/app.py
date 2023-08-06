import os
from flask import Flask


def create_app():
    # don't change import unless you know how it works
    from . import errors, wiki
    app = Flask(__name__)
    errors.register_errors(app)
    app.register_blueprint(wiki.bp)
    return app
