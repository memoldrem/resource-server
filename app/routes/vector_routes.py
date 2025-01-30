from flask import Blueprint, request, jsonify
from openai import OpenAI
from app.database.pinecone import index 
import os

vectors_bp = Blueprint('vector', __name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@vectors_bp.route('/search', methods=['GET'])
def search_posts():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        # Convert query to embedding
        response = client.embeddings.create(input=[query], model="text-embedding-ada-002")
        query_vector = response.data[0].embedding  

        # Perform vector search in Pinecone
        results = index.query(vector=query_vector, top_k=10, include_metadata=True)

        # Set a similarity score threshold
        min_score = 0.5  
        filtered_results = [
            {"post_id": match["id"], "score": match["score"], "content": match["metadata"].get("content")}
            for match in results['matches'] if match["score"] >= min_score
        ]

        # Fallback to keyword search if no results found
        # if not filtered_results:
        #     fallback_results = list(db.posts.find(
        #         {"content": {"$regex": query, "$options": "i"}}
        #     ).limit(5))

        #     filtered_results = [
        #         {"post_id": str(post["_id"]), "content": post["content"]}
        #         for post in fallback_results
        #     ]

        if not filtered_results:
            return jsonify({'message': 'No relevant posts found'}), 200

        return jsonify(filtered_results)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



# @vectors_bp.route('/recommend', methods=['GET'])
# def recommend_posts():
#     post_id = request.args.get('post_id')
#     if not post_id:
#         return jsonify({'error': 'Post ID is required'}), 400
#     try:
#         # Retrieve the embedding for the given post
#         result = index.fetch(ids=[post_id])
#         if not result or 'vectors' not in result or post_id not in result['vectors']:
#             return jsonify({'error': 'Post not found or embedding not available'}), 404

#         post_embedding = result['vectors'][post_id]['values']

#         # Perform recommendation based on similarity
#         recommendations = index.query(vector=post_embedding, top_k=5, include_metadata=True)

#         if not recommendations.get('matches'):
#             return jsonify({'message': 'No similar posts found'}), 200

#         refined_recommendations = [
#             {"post_id": match["id"], "score": match["score"], "content": match["metadata"].get("content")}
#             for match in recommendations['matches']
#         ]
        
#         return jsonify(refined_recommendations)
#     except Exception as e:
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500



# @vectors_bp.route('/detect_spam', methods=['POST'])
# def detect_spam():
#     post_content = request.json.get('content')
#     if not post_content:
#         return jsonify({'error': 'Post content is required'}), 400
    
#     # Detect spam using a pre-trained model (you can use NLP models like BERT for this)
#     is_spam = some_spam_detection_model.predict(post_content)
    
#     # Store the spam flag (either in Pinecone or a database)
#     if is_spam:
#         mark_post_as_spam(post_content)
    
#     return jsonify({'is_spam': is_spam})

# def mark_post_as_spam(content):
#     # Function to mark a post as spam (implement your storage logic)
#     print(f"Post marked as spam: {content}")
