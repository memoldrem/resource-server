from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import pytz
from mongo_db import db

ai_configs_collection = db['ai_configs']

# Utilities
def create_ai_config(assistant_name, config):
    ai_config = {
        "assistant_name": assistant_name,
        "config": config,
        "created_at": datetime.now(pytz.UTC),
        "updated_at": datetime.now(pytz.UTC),
    }
    return ai_configs_collection.insert_one(ai_config).inserted_id