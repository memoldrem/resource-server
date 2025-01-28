from bson import ObjectId
from datetime import datetime
import pytz
from app import mongo

class AIConfigRepository:

    @staticmethod  # Create 
    def store_assistant_config(config_type, assistant_name, model_name, additional_settings=None):
        """
        Parameters:
            - config_type (str): The type of assistant (e.g., "moderation", "user_support", "recommendation").
            - assistant_name (str): The name of the assistant (e.g., "Content Moderator", "User Query Assistant").
            - model_name (str): The LangChain model or tool to be used (e.g., "text-davinci", "gpt-3.5").
            - additional_settings (dict, optional): Any additional settings specific to the assistant type.
        """
        
        allowed_config_types = ["moderation", "user_support", "recommendation", "general"]
        allowed_model_names = ["text-davinci", "gpt-3.5", "gpt-4"]  # Adjust based on LangChain models you're using

        if config_type not in allowed_config_types:
            return {"error": "Invalid config_type provided."}
        if model_name not in allowed_model_names:
            return {"error": "Invalid model_name provided."}

        # Prepare configuration document
        config_collection = mongo.db.ai_assistants
        new_config = {
            "config_type": config_type,
            "assistant_name": assistant_name,
            "model_name": model_name,
            "settings": additional_settings or {},  # Allow empty settings if not provided
            "created_at": datetime.now(pytz.UTC),
            "updated_at": datetime.now(pytz.UTC),
        }

        config_id = config_collection.insert_one(new_config).inserted_id
        
        print(f'AI Assistant Config added with ID {str(config_id)}')
        return {
            "id": str(config_id),
            "config_type": config_type,
            "assistant_name": assistant_name,
            "model_name": model_name,
            "settings": additional_settings or {},
            "success": True,
        }

    @staticmethod  # Get 
    def get_assistant_config_by_id(config_id):
        config_collection = mongo.db.ai_assistants
        config = config_collection.find_one({"_id": ObjectId(config_id)})
        
        if config:
            config['_id'] = str(config['_id'])
            return config
        return None

    @staticmethod  # Get all AI Assistant Configurations by type
    def get_assistants_by_type(config_type):
        config_collection = mongo.db.ai_assistants
        configs = config_collection.find({"config_type": config_type})
        
        assistants = []
        for config in configs:
            config['_id'] = str(config['_id'])  
            assistants.append(config)
        
        return assistants

    @staticmethod  # Update 
    def update_config(config_id, updated_fields):
        config_collection = mongo.db.ai_assistants
        updated_fields["updated_at"] = datetime.now(pytz.UTC)

        try:
            result = config_collection.update_one(
                {"_id": ObjectId(config_id)},
                {"$set": updated_fields}
            )

            if result.modified_count > 0:
                # Fetch the updated configuration for clarity
                updated_config = config_collection.find_one({"_id": ObjectId(config_id)})
                updated_config["_id"] = str(updated_config["_id"])  
                return {"success": True, "message": "Configuration updated", "config": updated_config}

            return {"success": False, "message": "Configuration not found or no changes made"}
        except Exception as e:
            return {"success": False, "message": f"Error updating configuration: {str(e)}"}

    @staticmethod  # Delete 
    def delete_config(config_id):
        try:
            config_object_id = ObjectId(config_id) 
            config_collection = mongo.db.ai_assistants
            result = config_collection.delete_one({"_id": config_object_id})

            if result.deleted_count == 1:
                return {"message": "Configuration deleted successfully", "success": True}
            else:
                return {"message": "Configuration not found", "success": False}
        except Exception as e:
            return {"message": f"Error deleting configuration: {str(e)}", "success": False}

    @staticmethod  # Delete all AI Assistant Configurations of a specific type
    def delete_configs_by_type(config_type):
        try:
            config_collection = mongo.db.ai_assistants
            result = config_collection.delete_many({"config_type": config_type})

            return {"message": f"Deleted {result.deleted_count} configurations", "success": True}
        except Exception as e:
            return {"message": f"Error deleting configurations: {str(e)}", "success": False}