from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from app.config import Config
from flask_migrate import Migrate



db = SQLAlchemy()
mongo = PyMongo()

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    mongo.init_app(app)
    migrate = Migrate(app, db)
    
    # Register Blueprints
    from app.routes.forum_routes import forums_bp
    from app.routes.thread_routes import threads_bp
    from app.routes.post_routes import posts_bp
    app.register_blueprint(forums_bp, url_prefix='/')
    app.register_blueprint(threads_bp, url_prefix='/')
    app.register_blueprint(posts_bp, url_prefix='/')
    
    return app

