from flask_pymongo import PyMongo
from flask import current_app
from bson import ObjectId
from datetime import datetime
import pytz

class PostRepository:
    @staticmethod # Create
    def create_post(content, thread_id, author_id):
        posts_collection = current_app.mongo.db.posts
        new_post = {
            "thread_id": thread_id,
            "author_id": author_id,
            "content": content,
            "created_at": datetime.now(pytz.UTC),
            "updated_at": datetime.now(pytz.UTC),
        }
        
        post_id = posts_collection.insert_one(new_post).inserted_id
        return { "id": str(post_id), "content": content, "thread_id": thread_id }

    @staticmethod # Read
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
    
    @staticmethod   # Update
    def update_post(post_id: str, content: str):
        try:
            post_object_id = ObjectId(post_id) # Convert post_id to ObjectId
            posts_collection = current_app.mongo.db.posts
            result = posts_collection.update_one(
                {"_id": post_object_id},
                {"$set": {"content": content, "updated_at": datetime.now(pytz.UTC)}}
            )
            if result.modified_count == 1:
                return {"message": "Post updated successfully", "success": True}
            else:
                return {"message": "Post not found", "success": False}
        except Exception as e:
            return {"message": f"Error updating post: {str(e)}", "success": False}


    @staticmethod   # Delete
    def delete_post(post_id: str):
        try:
            post_object_id = ObjectId(post_id) # Convert post_id to ObjectId
            posts_collection = current_app.mongo.db.posts
            result = posts_collection.delete_one({"_id": post_object_id})

            if result.deleted_count == 1:
                return {"message": "Post deleted successfully", "success": True}
            else:
                return {"message": "Post not found", "success": False}
        except Exception as e:
            return {"message": f"Error deleting post: {str(e)}", "success": False}
        
    
    @staticmethod
    def delete_posts_by_thread(thread_id: str):
        try:
            posts_collection = current_app.mongo.db.posts
            result = posts_collection.delete_many({"thread_id": thread_id})

            return {"message": f"Deleted {result.deleted_count} posts", "success": True}
        except Exception as e:
            return {"message": f"Error deleting posts: {str(e)}", "success": False}
