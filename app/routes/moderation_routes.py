from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from app.database.mongo_db import db 
load_dotenv()

moderation_bp = Blueprint("moderation", __name__)
config_collection = db["ai_assistants"]
openai_api_key = os.getenv("OPENAI_API_KEY")

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

    llm = OpenAI(
        model_name=model_name,
        max_tokens=max_tokens,
        temperature=temperature
    )

    # Define moderation prompt
    prompt = PromptTemplate(
        input_variables=["content"],
        template=(
            "You are a content moderation assistant. Analyze the following content for profanity, spam, "
            "and inappropriate language. Respond with a JSON object listing detected issues and their severity.\n\n"
            "Content: {content}\n\n"
            "Response:"
        )
    )


    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        moderation_response = chain.run(content)
    except Exception as e:
        return jsonify({"error": "Error processing content", "details": str(e)}), 500

    return jsonify({"content": content, "moderation_response": moderation_response}), 200
