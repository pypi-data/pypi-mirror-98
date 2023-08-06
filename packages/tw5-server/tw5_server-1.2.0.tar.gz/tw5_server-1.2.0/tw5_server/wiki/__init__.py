from flask import Blueprint

bp = Blueprint('wiki', __name__)

from . import views
