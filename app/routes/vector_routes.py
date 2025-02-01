from bson import ObjectId
from flask import Blueprint, request, jsonify
from openai import OpenAI
from app.database.pinecone import index 
from transformers import pipeline
from app import mongo
import os

vectors_bp = Blueprint('vector', __name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pipe = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")

@vectors_bp.route('/search', methods=['GET'])
def search_posts():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        # Convert query to embedding
        response = client.embeddings.create(input=[query], model="text-embedding-ada-002")
        query_vector = response.data[0].embedding  

        results = index.query(vector=query_vector, top_k=10, include_metadata=True)

        min_score = 0.5  
        filtered_results = [
            {"post_id": match["id"], "score": match["score"], "content": match["metadata"].get("content")}
            for match in results['matches'] if match["score"] >= min_score
        ]

        if not filtered_results:
            return jsonify({'message': 'No relevant posts found'}), 200

        return jsonify(filtered_results)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



@vectors_bp.route('/recommend/<post_id>', methods=['GET'])
def recommend_posts(post_id):
    if not post_id:
        return jsonify({'error': 'Post ID is required'}), 400
    try:
        # Retrieve the embedding for the given post
        result = index.fetch(ids=[post_id])
        if not result or 'vectors' not in result or post_id not in result['vectors']:
            return jsonify({'error': 'Post not found or embedding not available'}), 404

        post_embedding = result['vectors'][post_id]['values']

        # Perform recommendation based on similarity
        recommendations = index.query(vector=post_embedding, top_k=5, include_metadata=True)

        if not recommendations.get('matches'):
            return jsonify({'message': 'No similar posts found'}), 200
        

        refined_recommendations = [
            {"post_id": match["id"], "score": match["score"], "content": match["metadata"].get("content"), 
             "thread_id": match["metadata"].get("thread_id"), "author_id": match["metadata"].get("author_id")}
            for match in recommendations['matches']
            if match["id"] != post_id
        ]
        
        return refined_recommendations
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    

def recommend_threads(post_id):
    if not post_id:
        print("Error: Post ID is required")
        return {"error": "Post ID is required"}
    
    try:
        # Fetch the embedding for the given post
        result = index.fetch(ids=[post_id])

        if not result or 'vectors' not in result or post_id not in result['vectors']:
            print("Error: Post not found or embedding not available")
            return {"error": "Post not found or embedding not available"}

        post_embedding = result['vectors'][post_id]['values']

        threads = []

        # Perform similarity query
        recommendations = index.query(vector=post_embedding, top_k=50, include_metadata=True)
        # print(f"Raw recommendations: {recommendations}")  # Debugging

        if not recommendations.get('matches'):
            print("No similar posts found")
            return {"message": "No similar posts found"}

        for match in recommendations['matches']:
            # print(f"Match found: {match}")  # Debugging

            # Check metadata structure
            if "metadata" not in match:
                # print("Skipping match due to missing metadata:", match)
                continue

            thread_id = match["metadata"].get("thread_id")  # Safe way to access metadata
            # print(f"Extracted thread_id: {thread_id}")  # Debugging

            if not thread_id:
                print(f"Skipping match due to missing thread_id: {match}")  # Debugging
                continue

            if thread_id in threads:
                continue

            threads.append(thread_id)
            # print(f"Added thread_id: {thread_id}")  # Debugging

            if len(threads) >= 5:
                break

        # print(f"Final recommended threads: {threads}")  # Debugging
        return threads

    except Exception as e:
        print(f"Exception occurred: {str(e)}")  # Debugging
        return {"error": f"An error occurred: {str(e)}"}





@vectors_bp.route('/detect_spam/<post_id>', methods=['POST'])
def detect_spam(post_id):
    
    post_collection = mongo.db.posts # to get post content
    post = post_collection.find_one({"_id": ObjectId(post_id)})
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    post_content = post.get("content")
    if not post_content:
        return jsonify({'error': 'Post content is missing'}), 404
    
    result = pipe(post_content) # via huggingface
    is_spam = result[0]['label'] == 'LABEL_1' # label 1 = spam
    
    # If the post is marked as spam, update the status in mongo + pinecoen
    if is_spam:
        mark_post_as_spam(post_content, post_id)
    return jsonify({'is_spam': is_spam})

def mark_post_as_spam(content, post_id):
    print(f"Post marked as spam: {content}")
    
    post_collection = mongo.db.posts # hey mongo
    post_collection.update_one(
        {"post_id": post_id}, 
        {"$set": {"is_spam": True}}  
    )
   
    response = client.embeddings.create(input=[content], model="text-embedding-ada-002")
    embedding = response.data[0].embedding  # Extract the embedding
    
    # Update with the spam flag in Pinecone
    upsert_response = index.upsert(vectors=[{
        'id': post_id,
        'values': embedding,
        'metadata': {"content": content, "is_spam": True}  # Mark as spam
    }])
    
    print("Upsert Response:", upsert_response) 