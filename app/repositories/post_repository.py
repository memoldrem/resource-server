from flask_pymongo import PyMongo
from flask import current_app
from datetime import datetime
import pytz

class PostRepository:
    @staticmethod
    def create_post(content, thread_id, author_id):
        # Access MongoDB collection 'posts'
        posts_collection = current_app.mongo.db.posts
        
        new_post = {
            "thread_id": thread_id,
            "author_id": author_id,
            "content": content,
            "created_at": datetime.now(pytz.UTC),
            "updated_at": datetime.now(pytz.UTC),
        }
        
        # Insert the new post into the 'posts' collection
        post_id = posts_collection.insert_one(new_post).inserted_id
        
        # Return the created post with its ID
        return { "id": str(post_id), "content": content, "thread_id": thread_id }

    @staticmethod
    def get_post_by_id(post_id):
        posts_collection = current_app.mongo.db.posts
        post = posts_collection.find_one({"_id": post_id})
        
        if post:
            post['_id'] = str(post['_id'])  # Convert ObjectId to string for JSON serialization
            return post
        return None

    @staticmethod
    def get_posts_by_thread(thread_id):
        posts_collection = current_app.mongo.db.posts
        posts_cursor = posts_collection.find({"thread_id": thread_id})
        
        posts = []
        for post in posts_cursor:
            post['_id'] = str(post['_id'])  
            posts.append(post)
        
        return posts
    

    @staticmethod
    def get_posts_by_author(author_id):
        
        posts_collection = current_app.mongo.db.posts 
        posts_cursor = posts_collection.find({"author_id": author_id})
        
        posts = [] 
        for post in posts_cursor:
            post['_id'] = str(post['_id'])  
            posts.append(post)
        
        return posts
