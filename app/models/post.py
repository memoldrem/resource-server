from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import pytz
from mongo_db import db

posts_collection = db['posts']


# Utility Functions
def create_post(thread_id, author_id, content):
    post = {
        "thread_id": thread_id,
        "author_id": author_id,
        "content": content,
        "created_at": datetime.now(pytz.UTC),
        "updated_at": datetime.now(pytz.UTC),
    }
    return posts_collection.insert_one(post).inserted_id


def get_posts_by_thread(thread_id):
    """Retrieve all posts in a specific thread."""
    return list(posts_collection.find({"thread_id": thread_id}))


def get_post_by_id(post_id):
    """Retrieve a single post by its ID."""
    return posts_collection.find_one({"_id": ObjectId(post_id)})


def update_post(post_id, content):
    return posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {"content": content, "updated_at": datetime.now(pytz.UTC)}}
    )


def delete_post(post_id):
    return posts_collection.delete_one({"_id": ObjectId(post_id)})




