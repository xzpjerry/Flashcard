from flask import Flask
from flask_wtf import FlaskForm
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

#######################
#### Configuration ####
#######################

db = SQLAlchemy()
login_manager = LoginManager()

######################################
#### Application Factory Function ####
######################################

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    return app

##########################
#### Helper Functions ####
##########################

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)

    db.init_app(app)

    # Flask-Login configuration
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'users.login'
    login_manager.init_app(app=app)
    from Flashcard.models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    app.app_context().push()

def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from Flashcard.cards_learning import cards_learning_blueprint
    from Flashcard.users import users_blueprint
    app.register_blueprint(cards_learning_blueprint)
    app.register_blueprint(users_blueprint)