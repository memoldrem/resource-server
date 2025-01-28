from flask import Blueprint, request, jsonify, json
from openai import OpenAI
import os
from dotenv import load_dotenv
from app import mongo

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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

    model_name = config.get("model_name", "gpt-3.5-turbo")  # Default to gpt-3.5
    max_tokens = config["settings"].get("max_tokens", 1500)
    temperature = config["settings"].get("temperature", 0.6)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a strict content moderation assistant. Please analyze the content provided and return the result in the following structured JSON format, along with a general moderation comment:"},
                {"role": "system", "content": """
                {
                    "toxicity": "toxic" or "neutral",  # Mark as 'toxic' for harmful, derogatory, or insulting language
                    "violence": "violent" or "safe",   # Mark as 'violent' if there is any incitement or promotion of violence
                    "hate_speech": "offensive" or "neutral",  # Mark as 'offensive' for hate speech, even if indirect or subtle
                    "overall": "flagged" or "safe",  # Mark as 'flagged' if any of the categories are harmful
                    "general_feedback": "Provide clear reasoning for the content moderation decision, with a focus on sensitivity and inclusivity."
                }
                """},  
                {"role": "user", "content": content}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
      
        moderation_response = response.choices[0].message.content.strip()
        moderation_response = moderation_response.replace("\n", " ")
        # print("Moderation response:", moderation_response)
        moderation_response_dict = json.loads(moderation_response)

        # Return content with the moderation response
        if moderation_response_dict.get("overall") == "flagged":
            return jsonify({"content": content, "flagged": True, "moderation_response": moderation_response}), 200
        return jsonify({"content": content, "flagged": False, "moderation_response": moderation_response}), 200

    except Exception as e:
        return jsonify({"error": "Error processing content", "details": str(e)}), 500
