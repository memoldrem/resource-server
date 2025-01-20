from app import db
from datetime import datetime
import pytz

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC), onupdate=datetime.now(pytz.UTC))
    
    # Relationship: A Category has many Forums
    forums = db.relationship('Forum', backref='category', lazy=True)


class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC), onupdate=datetime.now(pytz.UTC))
    
    # Foreign Key for Category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Foreign Key for UserRole (author of the forum)
    author_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)
    
    # Relationship: A Forum has many Threads
    threads = db.relationship('Thread', backref='forum', lazy=True)


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    post_count = db.Column(db.Integer, default=0)  # Tracks number of posts
    last_post_at = db.Column(db.DateTime)  # Tracks time of the last post
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(pytz.UTC), onupdate=datetime.now(pytz.UTC))
    
    # Foreign Key for Forum
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'), nullable=False)
    
    # Foreign Key for UserRole (author of the thread)
    author_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # E.g., admin, moderator, user


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)  # OAuth User ID
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
    # Relationship: A UserRole can have many Forums and Threads
    forums = db.relationship('Forum', backref='author', lazy=True)
    threads = db.relationship('Thread', backref='author', lazy=True)
