from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from enum import Enum
import datetime

from Flashcard import db

class Difficulty(Enum):
    Easy = 1
    Good = 0
    Again = -1
class Card(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    front = db.Column(db.Text)
    back = db.Column(db.Text)
    ease_factor = db.Column(db.Float, default = 1.1)
    interval_seconds = db.Column(db.Float, default = 60)
    due_date = db.Column(db.DateTime, index = True, default=datetime.datetime.utcnow)

    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))

    def update_due(self, with_difficulty : Difficulty):
        if with_difficulty is Difficulty.Easy:
            self.ease_factor += 0.15
        elif with_difficulty is Difficulty.Again:
            self.ease_factor -= 0.2
        self.interval_seconds *= self.ease_factor
        time_duration = datetime.timedelta(seconds=self.interval_seconds)
        self.due_date += time_duration
        self.due_date = self.due_date.replace(second=0, microsecond=0)
        db.session.commit()

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32))
    
    cards = db.relationship('Card', backref = db.backref('deck', lazy = True, uselist = False))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_next(self):
        return Card.query.filter(Card.deck_id == self.id and Card.due_date <= datetime.datetime.utcnow()).order_by(Card.due_date.asc()).first()

class User(UserMixin, db.Model):
    '''
    self.id : int
    self.userName : str
    self.credentials : str
    self.resume : Resume
    '''
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), unique = True)
    password = db.Column(db.String(100), nullable = False)

    decks = db.relationship('Deck', backref = db.backref('user', lazy = True, uselist = False))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_decks(self):
        return decks
