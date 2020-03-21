# from flask_login import UserMixin
from Flashcard import db
from enum import Enum
import datetime

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

    @classmethod
    def get_next(cls):
        return cls.query.filter(cls.due_date <= datetime.datetime.utcnow()).order_by(cls.due_date.asc()).first()

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

# class Deck(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     secret = db.Column(db.SmallInteger)
#     current_playing_video_ID = db.Column(db.String(24), default = 'QaQdY7iI75c')
#     current_isplaying = db.Column(db.Boolean, default = False)
#     current_seek = db.Column(db.Float, default=0.0)

#     owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     owner = db.relationship('User', foreign_keys=owner_id, backref = db.backref('owned_room', lazy = True, uselist = False, cascade="all, delete"), uselist=False, cascade="all, delete")
    
#     timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

#     @classmethod
#     def delete_expired(cls):
#         expiration_days = 1
#         limit = datetime.datetime.now() - datetime.timedelta(days=expiration_days)
#         cls.query.filter(cls.timestamp <= limit).delete()
#         db.session.commit()

#     def __repr__(self):
#         return 'Resume ' + str(self.id)

# class User(UserMixin, db.Model):
#     '''
#     self.id : int
#     self.userName : str
#     self.credentials : str
#     self.resume : Resume
#     '''
#     id = db.Column(db.Integer, primary_key = True)
#     session_id = db.Column(db.String(32), unique = True)
#     username = db.Column(db.String(32), unique = True)
#     room_id = db.Column(db.Integer, db.ForeignKey('room.id'), default=-1)
#     room = db.relationship('Room', foreign_keys=room_id, backref = db.backref('users', lazy = True, cascade='all, delete'), post_update=True, uselist=False)
#     timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

#     def __repr__(self):
#         return 'User ' + str(self.id) 