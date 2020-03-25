#################
#### imports ####
#################
import flask
from flask import render_template, redirect, flash, request, jsonify, abort
from flask_login import login_required, current_user, logout_user, login_user

from . import cards_learning_blueprint
from Flashcard import db
from Flashcard.models import Card, Difficulty, Deck

################
#### helpers ####
################

################
#### routes ####
################

@cards_learning_blueprint.route('/', methods=('GET',))
def index():
    decks = []
    if current_user.is_authenticated:
        for deck in current_user.decks:
            decks.append((deck.id, deck.name))
    return render_template('cards_learning_blueprint/index.html', decks=decks)

@cards_learning_blueprint.route('/learn/<int:deck_id>', methods=('GET',))
@login_required
def learn(deck_id):
    deck = Deck.query.filter_by(id = deck_id).first()
    if not deck or not deck.user_id == current_user.id:
        return abort(404)
    return render_template('cards_learning_blueprint/learn.html', card=deck.get_next())

@cards_learning_blueprint.route('/deck/add', methods=('POST',))
@login_required
def add_deck():
    code = 200
    res = {'success': True}
    data = request.form
    deck_name = data.get('name', False)
    if not deck_name:
        code = 401
        res['success'] = False
        res['errors'] = "You need a name for the deck!"
    else:
        new_deck = Deck(name=deck_name, user_id=current_user.id)
        db.session.add(new_deck)
        db.session.commit()
        res['deck_id'] = new_deck.id
        res['deck_name'] = deck_name
    return jsonify(res), code

@cards_learning_blueprint.route('/deck/rename/<int:deck_id>/<string:new_name>', methods=('PUT',))
@login_required
def rename_deck(deck_id, new_name):
    code = 200
    res = {'success': True}
    if not new_name or not deck_id:
        code = 401
        res['success'] = False
        res['errors'] = "No deck id or new name."
    else:
        deck = Deck.query.filter_by(id=deck_id, user_id=current_user.id).first()
        if not deck:
            code = 405
            res['success'] = False
            res['errors'] = "Invalid deck id."
        else:
            deck.name = new_name
            db.session.commit()
    return jsonify(res), code

@cards_learning_blueprint.route('/deck/delete/<int:deck_id>', methods=('DELETE',))
@login_required
def delete_deck(deck_id):
    code = 200
    res = {'success': True}
    if not deck_id:
        code = 401
        res['success'] = False
        res['errors'] = "No deck id."
    else:
        deck = Deck.query.filter_by(id=deck_id, user_id=current_user.id).first()
        if not deck:
            code = 405
            res['success'] = False
            res['errors'] = "Invalid deck id."
        else:
            db.session.delete(deck)
            db.session.commit()
    return jsonify(res), code

@cards_learning_blueprint.route('/card/add/<int:deck_id>', methods=('POST',))
@login_required
def add_card(deck_id):
    code = 200
    res = {'success': True}
    deck = Deck.query.filter_by(id = deck_id).first()
    if not deck:
        code = 401
        res['success'] = False
        res['errors'] = "Invalid deck id"
    else:
        data = request.form
        front = data.get('front', False)
        back = data.get('back', "")
        if not front:
            code = 401
            res['success'] = False
            res['errors'] = "You need to fill out at least the front side!"
        else:
            db.session.add(Card(front=front, back=back, deck_id=deck_id))
            db.session.commit()
    return jsonify(res), code


##############################
#### For Debuging Purpose ####
##############################
