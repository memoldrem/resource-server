from datetime import datetime
from app import mongo
from bson import ObjectId
import pytz

class AIConfigRepository:

    @staticmethod  # Create
    def store_assistant_config(config_type, model_name, additional_settings=None):
        """
        Store the AI assistant configuration.
        """
        config_collection = mongo.db.ai_assistants

        new_config = {
            "config_type": config_type,  # e.g., "moderation", "user_support"
            "model_name": model_name,    # e.g., "gpt-3.5-turbo"
            "settings": additional_settings or {},
            "created_at": datetime.now(pytz.UTC),
            "updated_at": datetime.now(pytz.UTC),
        }

        config_id = config_collection.insert_one(new_config).inserted_id
        print('AI Assistant Config added')
        return {"id": str(config_id), "config_type": config_type, "model_name": model_name}

    @staticmethod  # Read
    def get_config_by_id(config_id):
        """
        Retrieve a configuration by its ID.
        """
        config_collection = mongo.db.ai_assistants
        try:
            config = config_collection.find_one({"_id": ObjectId(config_id)})
        except Exception as e:
            print(f"Error converting config_id to ObjectId: {e}")
            return None
        
        if config:
            config['_id'] = str(config['_id'])  # Convert ObjectId to string for JSON serialization
            return config
        return None

    @staticmethod
    def get_configs_by_type(config_type):
        """
        Retrieve all configurations by type (e.g., "moderation").
        """
        config_collection = mongo.db.ai_assistants
        print(f"Searching for AI assistant configs with config_type: {config_type}")
        configs_cursor = config_collection.find({"config_type": config_type})

        configs = []
        for config in configs_cursor:
            config['_id'] = str(config['_id'])  # Convert ObjectId to string
            configs.append(config)

        return configs

    @staticmethod  # Update
    def update_config(config_id, updated_fields):
        """
        Update the AI assistant configuration.
        """
        config_collection = mongo.db.ai_assistants
        updated_fields["updated_at"] = datetime.now(pytz.UTC)

        result = config_collection.update_one(
            {"_id": ObjectId(config_id)},
            {"$set": updated_fields}
        )

        if result.modified_count > 0:
            return {"success": True, "message": "Configuration updated", "config": updated_fields}
        return {"success": False, "message": "Configuration not found or no changes made"}

    @staticmethod  # Delete
    def delete_config(config_id):
        """
        Delete a specific AI assistant configuration.
        """
        try:
            config_object_id = ObjectId(config_id)  # Convert config_id to ObjectId
            config_collection = mongo.db.ai_assistants
            result = config_collection.delete_one({"_id": config_object_id})

            if result.deleted_count == 1:
                return {"message": "Configuration deleted successfully", "success": True}
            else:
                return {"message": "Configuration not found", "success": False}
        except Exception as e:
            return {"message": f"Error deleting configuration: {str(e)}", "success": False}

    @staticmethod
    def delete_configs_by_type(config_type):
        """
        Delete all configurations of a specific type (e.g., "moderation").
        """
        try:
            config_collection = mongo.db.ai_assistants
            result = config_collection.delete_many({"config_type": config_type})

            return {"message": f"Deleted {result.deleted_count} configurations", "success": True}
        except Exception as e:
            return {"message": f"Error deleting configurations: {str(e)}", "success": False}
