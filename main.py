from Flashcard import create_app

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/flask.cfg
app = create_app('dev.cfg')
if app.config.get('TESTING', False):
    from Flashcard import db
    db.create_all()
app.run(host='0.0.0.0', port=5000)