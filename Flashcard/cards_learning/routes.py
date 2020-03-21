#################
#### imports ####
#################
import flask
from flask import render_template, redirect, flash, request, jsonify, abort
# from flask_login import login_required, current_user, logout_user, login_user

from . import cards_learning_blueprint
from Flashcard import db
from Flashcard.models import Card, Difficulty

################
#### helpers ####
################

################
#### routes ####
################

@cards_learning_blueprint.route('/', methods=('GET',))
def index():
    return render_template('cards_learning_blueprint/index.html', card=Card.get_next())

@cards_learning_blueprint.route('/add', methods=('POST',))
def add_card():
    data = request.form
    front = data.get('front', False)
    back = data.get('back', False)
    code = 200
    res = {'success': True}
    if not front or not back:
        code = 401
        res['success'] = False
    else:
        db.session.add(Card(front=front, back=back))
        db.session.commit()
    return jsonify(res), code


##############################
#### For Debuging Purpose ####
##############################
