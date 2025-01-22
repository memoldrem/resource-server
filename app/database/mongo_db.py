from pymongo import MongoClient
import os

# Initialize the MongoDB connection and return the database
def get_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/") # rn it's localhost
    client = MongoClient(mongo_uri)
    return client['forum_management']

db = get_db()
