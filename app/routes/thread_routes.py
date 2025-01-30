from flask import Blueprint, request, jsonify
from app.repositories.thread_repository import ThreadRepository
from app.repositories.post_repository import PostRepository


threads_bp = Blueprint('threads', __name__)
post_repo = PostRepository()


@threads_bp.route('/threads', methods=['POST']) # create
def create_thread():
    data = request.get_json()
    try:
        title = data['title']
        forum_id = data['forum_id']
        author_id = data['author_id']
        new_thread = ThreadRepository.create_thread(title, forum_id, author_id)
        return jsonify({
            'id': new_thread.id,
            'title': new_thread.title,
            'post_count': new_thread.post_count,
            'last_post_at': new_thread.last_post_at,
            'created_at': new_thread.created_at,
            'updated_at': new_thread.updated_at,
            'forum_id': new_thread.forum_id,
            'author_id': new_thread.author_id
        }), 201
    except KeyError as e:
        return jsonify({'error': f"Missing field: {e}"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@threads_bp.route('/threads/<int:thread_id>', methods=['GET']) # Read
def get_thread(thread_id):
    try:
        thread = ThreadRepository.get_thread_by_id(thread_id)
        return jsonify({
            'id': thread.id,
            'title': thread.title,
            'post_count': thread.post_count,
            'last_post_at': thread.last_post_at,
            'created_at': thread.created_at,
            'updated_at': thread.updated_at,
            'forum_id': thread.forum_id,
            'author_id': thread.author_id
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    

@threads_bp.route('/threads/forum/<int:forum_id>', methods=['GET'])
def get_threads_by_forum(forum_id):
    threads = ThreadRepository.get_threads_by_forum(forum_id)
    if not threads:
            return jsonify({"message": "No threads found for this forum"}), 404
    
    return jsonify([{
        'id': thread.id,
        'title': thread.title,
        'post_count': thread.post_count,
        'last_post_at': thread.last_post_at,
        'created_at': thread.created_at,
        'updated_at': thread.updated_at,
        'forum_id': thread.forum_id,
        'author_id': thread.author_id
    } for thread in threads])


@threads_bp.route('/threads/<int:thread_id>/posts', methods=['POST']) # Update
def add_post_to_thread(thread_id):
    data = request.get_json()
    try:
        author_id = data['author_id']
        content = data['content']
        post = ThreadRepository.add_post_to_thread(post_repo, thread_id, author_id, content)
        return jsonify(post), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        print('thread_routes.py')
        return jsonify({'error': str(e)}), 500

@threads_bp.route('/threads/<int:thread_id>', methods=['DELETE'])
def delete_thread(thread_id):
    try:
        message = ThreadRepository.delete_thread(thread_id)
        return jsonify({'message': message})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500