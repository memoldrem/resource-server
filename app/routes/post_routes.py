from flask import Blueprint, redirect, request, jsonify, session, url_for
from openai import OpenAI
from app.repositories.post_repository import PostRepository
from app.utils.auth import token_required
from app.database.pinecone import index 
import os

posts_bp = Blueprint('post', __name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@posts_bp.route('/forum/<int:forum_id>/thread/<int:thread_id>/create_post', methods=['POST'])  # create
# @token_required
def create_post(forum_id, thread_id):
    PostRepository.create_post(content=request.form['content'], thread_id=thread_id, author_id=session.get('user_id'))
    return redirect(url_for('threads.view_thread', forum_id=forum_id, thread_id=thread_id))
    


# @posts_bp.route('/post/<post_id>', methods=['GET']) # Read
# # @token_required
# def get_post(post_id):
#     post = PostRepository.get_post_by_id(post_id)
#     if post:
#         return jsonify(post), 200
#     return jsonify({"message": "Post not found"}), 404


# @posts_bp.route('/thread/<thread_id>/posts', methods=['GET'])
# # @token_required
# def get_posts_by_thread(thread_id):
#     posts = PostRepository.get_posts_by_thread(thread_id)
#     return jsonify(posts), 200


@posts_bp.route('/author/<author_id>/posts', methods=['GET'])
# @token_required
def get_posts_by_author(author_id):
    posts = PostRepository.get_posts_by_author(author_id)
    return jsonify(posts), 200


@posts_bp.route('/forum/<int:forum_id>/thread/<int:thread_id>/post/<int:post_id>', methods=['PUT']) # update
# @token_required
def update_post(forum_id, thread_id, post_id):
    updated_fields = {"content": request.form['content']}  # Modify this depending on which fields you want to update
    result = PostRepository.update_post(post_id=post_id, updated_fields=updated_fields)
    if result.get("success"):
        return redirect(url_for('threads.view_thread', forum_id=forum_id, thread_id=thread_id))
    return jsonify({"message": result.get("message")}), 400


@posts_bp.route('/forum/<int:forum_id>/thread/<int:thread_id>/post/<int:post_id>', methods=['DELETE']) # delete
# @token_required
def delete_post(forum_id, thread_id, post_id):
    PostRepository.delete_post(post_id)
    return redirect(url_for('threads.view_thread', forum_id=forum_id, thread_id=thread_id))
    
