from flask import Blueprint, request, jsonify
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from app import mongo
load_dotenv()

moderation_bp = Blueprint("moderation", __name__)
config_collection = mongo.db.ai_assistants

@moderation_bp.route('/', methods=['POST'])
def moderate_content():
    content = request.json.get("content")

    if not content:
        return jsonify({"error": "Content is required"}), 400

    config = config_collection.find_one({"config_type": "moderation"})
    if not config:
        return jsonify({"error": "Moderation configuration not found"}), 500

    model_name = config.get("model_name", "gpt-3.5")
    max_tokens = config["settings"].get("max_tokens", 1500)
    temperature = config["settings"].get("temperature", 0.6)

    try:
        # Make API request to OpenAI's completion endpoint
        response = client.chat.completions.create(model=model_name,
        messages=[
            {"role": "system", "content": "You are a content moderation assistant."},
            {"role": "user", "content": content}
        ],
        max_tokens=max_tokens,
        temperature=temperature)

        moderation_response = response.choices[0].text
        return jsonify({"content": content, "moderation_response": moderation_response}), 200

    except Exception as e:
        return jsonify({"error": "Error processing content", "details": str(e)}), 500