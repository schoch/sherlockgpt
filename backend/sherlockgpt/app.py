from flask import Flask, session
from flask_session import Session
from cachelib.file import FileSystemCache
from backend.sherlockgpt.routes import initialize_routes
from flask_sqlalchemy import SQLAlchemy
from .database import db

app = Flask(__name__, static_folder='../../frontend', static_url_path='/frontend', template_folder='../../frontend')

# DB configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scenarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration
app.config['SESSION_TYPE']  = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] =  db

db.init_app(app)

# Import the models after db init
from backend.sherlockgpt.models import Scenario, Character

# Create db if not already done
with app.app_context():
    db.create_all()

Session(app)

initialize_routes(app)

if __name__ == '__main__':
    app.run(debug=True)