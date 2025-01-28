from flask import Blueprint, request, jsonify
from app.repositories.ai_assistant_repository import AIConfigRepository  # import the repository

ai_assistant_bp = Blueprint('ai_assistant', __name__)

# Create AI Assistant Configuration
@ai_assistant_bp.route('/', methods=['POST'])
def create_ai_assistant_config():
    data = request.get_json()
    config_type = data.get("config_type")
    assistant_name = data.get("assistant_name")
    model_name = data.get("model_name")
    additional_settings = data.get("settings", {})

    # Call the repository to store the assistant config
    result = AIConfigRepository.store_assistant_config(
        config_type=config_type,
        assistant_name=assistant_name,
        model_name=model_name,
        additional_settings=additional_settings
    )

    if result.get("success"):
        return jsonify(result), 201
    else:
        return jsonify(result), 400  # Return 400 if the creation failed

@ai_assistant_bp.route('/config/<config_type>', methods=['GET'])
def get_ai_assistants_by_config(config_type):
    allowed_config_types = ["moderation", "user_support", "recommendation", "general"]

    if config_type not in allowed_config_types:
        return {"error": "Invalid config_type provided."}

    res = AIConfigRepository.get_assistants_by_type(config_type)
    if res:
        return jsonify(res), 200
    return jsonify({"message": "No configurations found"}), 404


# Get a specific AI Assistant Configuration by ID
@ai_assistant_bp.route('/<config_id>', methods=['GET'])
def get_ai_assistant_config(config_id):
    config = AIConfigRepository.get_assistant_config_by_id(config_id)

    if config:
        return jsonify(config), 200
    return jsonify({"message": "Config not found"}), 404

# Update an existing AI Assistant Configuration
@ai_assistant_bp.route('/<config_id>', methods=['PUT'])
def update_ai_assistant_config(config_id):
    """
    Update an existing AI assistant configuration.
    """
    data = request.get_json()
    updated_fields = data.get("settings", {})

    result = AIConfigRepository.update_config(config_id, updated_fields)

    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 404  # Return 404 if the configuration is not found or no changes made

@ai_assistant_bp.route('/<config_id>', methods=['DELETE']) # Delete
def delete_ai_assistant_config(config_id):
    result = AIConfigRepository.delete_config(config_id)

    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 404  # Return 404 if the config was not found

# Delete AI Assistant Configurations by type (e.g., "moderation", "user_support")
@ai_assistant_bp.route('/<config_type>', methods=['DELETE'])
def delete_ai_assistant_configs_by_type(config_type):
    result = AIConfigRepository.delete_configs_by_type(config_type)

    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 400  # Return 400 in case of errors
