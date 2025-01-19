# Initialize the Flask app.
# Load configurations and register blueprints (routes).

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

#Initialize SQLAlchemy with your app.


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    # Register Blueprints here
    return app
