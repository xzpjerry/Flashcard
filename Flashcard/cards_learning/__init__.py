"""
The recipes Blueprint handles the creation, modification, deletion,
and viewing of recipes for this application.
"""
from flask import Blueprint
cards_learning_blueprint = Blueprint('cards_learning', __name__, static_folder='static', template_folder='templates', static_url_path='/static/cards_learning')

from . import routes
