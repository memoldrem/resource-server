from app import db
from datetime import datetime
import pytz



class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC), onupdate=datetime.now(pytz.UTC))

    threads = db.relationship('Thread', backref='forum', lazy=True)


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    post_count = db.Column(db.Integer, default=0)  # Tracks number of posts
    last_post_at = db.Column(db.DateTime)  # Tracks time of the last post
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC), onupdate=datetime.now(pytz.UTC))
    

    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # E.g., admin, moderator, user


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)  # OAuth User ID
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
    threads = db.relationship('Thread', backref='author', lazy=True)
