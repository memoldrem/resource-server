from flask import Blueprint, request, jsonify
from app import db
from app.repositories.forum_repository import ForumRepository

forums_bp = Blueprint('forum', __name__)


@forums_bp.route('/forums', methods=['POST'])
#ADMIN ONLY MIDDLEWARE
def create_forum():
    data = request.get_json()
    try:
        name = data['name']
        description = data['description']
        new_forum = ForumRepository.create_forum(name, description)
        return jsonify({
            'id': new_forum.id,
            'name': new_forum.name,
            'description': new_forum.description
        }), 201
    except KeyError as e:
        return jsonify({'error': f"Missing field: {e}"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@forums_bp.route('/forums/<int:forum_id>', methods=['GET'])
#ADMIN ONLY MIDDLEWARE
def get_forum_by_id(forum_id):
    try:
        forum = ForumRepository.get_forum_by_id(forum_id)
        if not forum:
            return jsonify({'error': 'Forum not found'}), 404
        return jsonify({
            'id': forum.id,
            'name': forum.name,
            'description': forum.description
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@forums_bp.route('/forums', methods=['GET'])
#ADMIN ONLY MIDDLEWARE
def get_all_forums():
    try:
        forums = ForumRepository.get_all_forums()
        return jsonify([{
            'id': forum.id,
            'name': forum.name,
            'description': forum.description
        } for forum in forums])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@forums_bp.route('/forums/<int:forum_id>', methods=['PUT'])
#ADMIN ONLY MIDDLEWARE
def update_forum(forum_id):
    data = request.get_json()
    try:
        name = data['name']
        description = data['description']
        forum = ForumRepository.update_forum(forum_id, name, description)
        if not forum:
            return jsonify({'error': 'Forum not found'}), 404
        return jsonify({
            'id': forum.id,
            'name': forum.name,
            'description': forum.description
        })
    except KeyError as e:
        return jsonify({'error': f"Missing field: {e}"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@forums_bp.route('/forums/<int:forum_id>', methods=['DELETE'])
#ADMIN ONLY MIDDLEWARE
def delete_forum(forum_id):
    try:
        forum = ForumRepository.delete_forum(forum_id)
        if not forum:
            return jsonify({'error': 'Forum not found'}), 404
        return jsonify({'message': f'Forum with ID {forum_id} deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500





