from flask import Blueprint, request, jsonify, redirect
from flask import Flask, render_template, request, redirect, url_for
from app.repositories.forum_repository import ForumRepository
from app.repositories.thread_repository import ThreadRepository

forums_bp = Blueprint('forums', __name__)

@forums_bp.route('/header', methods=['GET'])
def header():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Authorization header is missing'}), 401
    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return jsonify({'message': 'Invalid Authorization header format'}), 401
    
    access_token = parts[1]
    return jsonify({'message': 'Token is valid', 'token': access_token}), 200
    

@forums_bp.route('/discover', methods=['GET'])
def get_all_forums():
    forums = ForumRepository.get_all_forums()
    return render_template('index.html', forums=forums)

@forums_bp.route('/create_forum', methods=['GET', 'POST'])
#ADMIN ONLY MIDDLEWARE
def create_forum():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        ForumRepository.create_forum(name, description) # only moderators can do it
        return redirect(url_for('index'))
    return render_template('create_forum.html') # if GET, render template

@forums_bp.route('/forums/<int:forum_id>', methods=['GET']) # pulling up a forum
def get_forum_by_id(forum_id):
    forum = ForumRepository.get_forum_by_id(forum_id)
    if not forum:
        return jsonify({'error': 'Forum not found'}), 404
    threads = ThreadRepository.get_threads_by_forum(forum_id)
    return render_template('view_forum.html', forum=forum, threads=threads) # what do we render if there are no threads?



@forums_bp.route('/forums/<int:forum_id>', methods=['PUT']) # need edit forum page
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





