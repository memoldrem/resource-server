from flask import Blueprint, request, jsonify
from app.repositories.post_repository import PostRepository
from app.utils.auth import token_required

posts_bp = Blueprint('post', __name__)


# @post_bp.route('/post', methods=['POST']) #create
# @token_required
# def create_post(current_user):
#     data = request.get_json()

#     # Validate input
#     if not data or 'content' not in data or 'thread_id' not in data:
#         return jsonify({"message": "Missing required fields"}), 400

#     result = PostRepository.create_post(content=data['content'], thread_id=data['thread_id'])
#     if result.get("success"):
#         return jsonify({"message": "Post created", "post": result.get("post")}), 201
#     return jsonify({"message": result.get("message")}), 400


@posts_bp.route('/<post_id>', methods=['GET']) # Read
@token_required
def get_post(post_id):
    post = PostRepository.get_post_by_id(post_id)
    if post:
        return jsonify(post), 200
    return jsonify({"message": "Post not found"}), 404


# Get all posts by thread ID
@posts_bp.route('/thread/<thread_id>', methods=['GET'])
@token_required
def get_posts_by_thread(thread_id):
    posts = PostRepository.get_posts_by_thread(thread_id)
    return jsonify(posts), 200


# Get all posts by author ID
@posts_bp.route('/author/<author_id>', methods=['GET'])
@token_required
def get_posts_by_author(author_id):
    posts = PostRepository.get_posts_by_author(author_id)
    return jsonify(posts), 200


@posts_bp.route('/<post_id>', methods=['PUT']) # update
@token_required
def update_post(post_id):
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({"message": "Missing required fields"}), 400

    result = PostRepository.update_post(post_id=post_id, updated_fields={"content": data['content']})
    if result.get("success"):
        return jsonify({"message": "Post updated", "post": result.get("post")}), 200
    return jsonify({"message": result.get("message")}), 400


@posts_bp.route('/<post_id>', methods=['DELETE']) # delete
@token_required
def delete_post(post_id):
    result = PostRepository.delete_post(post_id)
    if result.get("success"):
        return jsonify({"message": "Post deleted"}), 200
    return jsonify({"message": result.get("message")}), 400
