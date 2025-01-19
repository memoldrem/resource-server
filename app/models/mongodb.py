from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime 
import os

# initializes a MongoDB connection using a URI
def get_mongo_client():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    return MongoClient(mongo_uri)

# Initialize the database
client = get_mongo_client()
db = client['forum_management']

# Collections
posts_collection = db['posts']
ai_configs_collection = db['ai_configs']

# Utility Functions
def create_post(thread_id, author_id, content):
    """Insert a new post into the posts collection."""
    post = {
        "thread_id": thread_id,
        "author_id": author_id,
        "content": content,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    return posts_collection.insert_one(post).inserted_id


def get_posts_by_thread(thread_id):
    """Retrieve all posts in a specific thread."""
    return list(posts_collection.find({"thread_id": thread_id}))


def get_post_by_id(post_id):
    """Retrieve a single post by its ID."""
    return posts_collection.find_one({"_id": ObjectId(post_id)})


def update_post(post_id, content):
    """Update the content of a post."""
    return posts_collection.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": {"content": content, "updated_at": datetime.utcnow()}}
    )


def delete_post(post_id):
    """Delete a post by its ID."""
    return posts_collection.delete_one({"_id": ObjectId(post_id)})


def create_ai_config(name, config):
    """Store an AI assistant configuration."""
    ai_config = {
        "assistant_name": name,
        "config": config,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    return ai_configs_collection.insert_one(ai_config).inserted_id


def get_ai_config_by_name(name):
    """Retrieve an AI assistant configuration by its name."""
    return ai_configs_collection.find_one({"assistant_name": name})


def delete_ai_config_by_name(name):
    """Delete an AI assistant configuration by its name."""
    return ai_configs_collection.delete_one({"assistant_name": name})
