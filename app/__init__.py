from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_migrate import Migrate
from app.config import Config
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

db = SQLAlchemy()
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['MONGO_URI'] = os.getenv("MONGO_URI")
    
    # Initialize databases
    db.init_app(app)
    mongo.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    

    from app.routes.forum_routes import forums_bp
    from app.routes.thread_routes import threads_bp
    from app.routes.post_routes import posts_bp
    from app.routes.ai_config_routes import ai_assistant_bp
    from app.routes.moderation_routes import moderation_bp
    from app.routes.vector_routes import vectors_bp
    app.register_blueprint(forums_bp, url_prefix='/forums/')
    app.register_blueprint(threads_bp, url_prefix='/threads/')
    app.register_blueprint(posts_bp, url_prefix='/posts/')
    app.register_blueprint(ai_assistant_bp, url_prefix='/assistant/')
    app.register_blueprint(moderation_bp, url_prefix='/moderation/')
    app.register_blueprint(vectors_bp, url_prefix='/vector/')

    
    return app


