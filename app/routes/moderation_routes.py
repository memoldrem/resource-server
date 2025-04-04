from flask import Blueprint, render_template, request, jsonify
import os
import json
from dotenv import load_dotenv
from app.database.pinecone import index, gindex 
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import Pinecone 
from langchain_pinecone import PineconeVectorStore 


load_dotenv()

"""
Retrieval Augmented Generation - Content Moderation

- Using OpenAI for now instead of a dedicated moderation model
- Combining past approved posts + community guidelines for decision-making
"""

llm = ChatOpenAI(model_name="gpt-4", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

# provides the function by which we will embed the query
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

vectorstore_index = PineconeVectorStore(index=index, embedding=embeddings, text_key="content" )
vectorstore_gindex = PineconeVectorStore(index=gindex, embedding=embeddings, text_key="content")


# we need two different retrievers
retriever_index = vectorstore_index.as_retriever(search_kwargs={"k": 20})  # 20 relevant posts
retriever_gindex = vectorstore_gindex.as_retriever(search_kwargs={"k": 3})  # 3 relevant guidelines

qa_chain_index = RetrievalQA.from_chain_type(llm=llm, retriever=retriever_index)
qa_chain_gindex = RetrievalQA.from_chain_type(llm=llm, retriever=retriever_gindex)


moderation_bp = Blueprint("moderation", __name__)

@moderation_bp.route("/", methods=["POST"])
def moderate_content():
    content = request.json.get("content")

    if not content:
        return jsonify({"error": "Content is required"}), 400

    try:
       
        guidelines_context = qa_chain_gindex.invoke(f"What community guidelines are relevant to this post? Content: {content}")
        past_posts = qa_chain_index.invokes(f"What posts are relevant to this post? Content: {content}")


        prompt = f"""
        You are a strict content moderation assistant. Analyze the following content based on these community guidelines:

        Content: {content}
        Relevant Guidelines: {guidelines_context}
        Posts that have been approved in the past: {past_posts}

        Your analysis should include:
        - Whether the content is harmful, toxic, or violates guidelines.
        - A detailed reason explaining why.
        - A general moderation decision (flagged or safe).
        
        Return JSON in this format:
        {{
            "toxicity": "neutral" or "toxic",
            "violence": "safe" or "violent",
            "hate_speech": "neutral" or "offensive",
            "overall": "safe" or "flagged",
            "reason": "Explanation of why the content is flagged or safe."
        }}
        """

        # Invoke OpenAI llm
        response = llm.invoke(prompt)

        
        moderation_result = json.loads(response["choices"][0]["message"]["content"])

        return jsonify({
            "content": content,
            "flagged": moderation_result["overall"] == "flagged",
            "reason": moderation_result["reason"],
            "moderation_result": moderation_result
        }), 200

    except Exception as e:
        return jsonify({"error": "Error processing content", "details": str(e)}), 500


@moderation_bp.route("/chat", methods=["GET"])
def get_chat():
        return render_template("question.html")


@moderation_bp.route("/chat", methods=["POST"])
def chat():
    content = request.form.get("content")

    if not content:
        return jsonify({"error": "Query is required"}), 400

    try:
        past_posts = qa_chain_index.invoke(f"What posts are relevant to this post? Content: {content}")
        prompt = f"""
        You are a chatbot that aims to answer user questions about things being talked about on the platform.
        You are 

        Here is the question: {content}
        Relevant posts: {past_posts}

        Your analysis should include:
        - Cite posts where appropriate. 
        - If there is not enough information, volunteer what information you do have and say that you do not know.
        
        Return JSON in this format:
        {{
            "response": Your response to the user question. 
        }}
        """

        # Invoke OpenAI llm
        response = llm.invoke(prompt)

        # llm_response = json.loads(response["choices"][0]["message"]["content"])
        response_dict = json.loads(response.content) 
        

        return render_template("question.html", response=response_dict["response"])


    except Exception as e:
        return jsonify({"error": "Error processing content", "details": str(e)}), 500
