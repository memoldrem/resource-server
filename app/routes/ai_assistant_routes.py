from flask import Blueprint, request, jsonify
from app.repositories.ai_assistant_repository import AIConfigRepository  # import the repository

ai_assistant_bp = Blueprint('ai_assistant', __name__)


@ai_assistant_bp.route('/', methods=['POST']) # create
def create_ai_assistant_config():
    data = request.get_json()
    config_type = data.get("config_type")
    model_name = data.get("model_name")
    additional_settings = data.get("settings", {})

    result = AIConfigRepository.store_assistant_config(
        config_type=config_type,
        model_name=model_name,
        additional_settings=additional_settings
    )

    return jsonify(result), 201

@ai_assistant_bp.route('/<config_id>', methods=['GET'])
def get_ai_assistant_config(config_id):
    config = AIConfigRepository.get_config_by_id(config_id)

    if config:
        return jsonify(config), 200
    return jsonify({"message": "Config not found"}), 404



@ai_assistant_bp.route('/<config_id>', methods=['PUT']) # update
def update_ai_assistant_config(config_id):
    data = request.get_json()
    updated_fields = data.get("settings", {})

    result = AIConfigRepository.update_config(config_id, updated_fields)

    return jsonify(result), 200 if result["success"] else 404


@ai_assistant_bp.route('/<config_id>', methods=['DELETE']) # delete
def delete_ai_assistant_config(config_id):
    result = AIConfigRepository.delete_config(config_id)

    return jsonify(result), 200 if result["success"] else 404


