from flask import Blueprint, redirect, render_template, request, jsonify, session, url_for
from app.repositories.thread_repository import ThreadRepository
from app.repositories.post_repository import PostRepository
from app.repositories.forum_repository import ForumRepository
from app.routes.vector_routes import recommend_threads, recommend_posts

threads_bp = Blueprint('threads', __name__)
post_repo = PostRepository()


@threads_bp.route('/forum/<int:forum_id>/create_thread', methods=['GET', 'POST'])
def create_thread(forum_id):
    forum = ForumRepository.get_forum_by_id(forum_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author_id = session.get('user_id')  # Ensure user_id is stored in session during login
        thread = ThreadRepository.create_thread(title, forum_id, author_id=1)
        PostRepository.create_post(content, thread.id , author_id)
        return redirect(url_for('forums.get_forum_by_id', forum_id=forum.id)) # go back out to forum home page
    return render_template('create_thread.html', forum=forum)
        
    
@threads_bp.route('forum/<int:forum_id>/threads/<int:thread_id>', methods=['GET'])  # Read
def view_thread(forum_id, thread_id):
    forum = ForumRepository.get_forum_by_id(forum_id)
    thread = ThreadRepository.get_thread_by_id(thread_id)
    posts = PostRepository.get_posts_by_thread(thread_id)
    recommendations = []

    if posts and isinstance(posts[0], dict):
        post_id = posts[0].get('_id') 

        
        if post_id:  
            thread_ids = recommend_threads(post_id)
            print('1111')
            print(recommend_threads(post_id))
        for i in thread_ids:
            th = ThreadRepository.get_thread_by_id(i)
            print(th.title)
            recommendations.append(ThreadRepository.get_thread_by_id(i))
    
    return render_template('view_thread.html', forum=forum, thread=thread, posts=posts, recommendations=recommendations)



@threads_bp.route('/forum/<int:forum_id>/threads/<int:thread_id>', methods=['DELETE'])
def delete_thread(forum_id, thread_id):
    ThreadRepository.delete_thread(thread_id)
    forum = ForumRepository.get_forum_by_id(forum_id)
    return redirect(url_for('view_forum', forum_id=forum.id))

    

# @threads_bp.route('/threads/forum/<int:forum_id>', methods=['GET'])
# def get_threads_by_forum(forum_id):
#     threads = ThreadRepository.get_threads_by_forum(forum_id)
#     if not threads:
#             return jsonify({"message": "No threads found for this forum"}), 404
    
#     return jsonify([{
#         'id': thread.id,
#         'title': thread.title,
#         'post_count': thread.post_count,
#         'last_post_at': thread.last_post_at,
#         'created_at': thread.created_at,
#         'updated_at': thread.updated_at,
#         'forum_id': thread.forum_id,
#         'author_id': thread.author_id
#     } for thread in threads])


# @threads_bp.route('forum/<int:forum_id>/threads/<int:thread_id>/posts', methods=['POST']) # Update
# def add_post_to_thread(forum_id, thread_id):
#     data = request.get_json()
#     try:
#         author_id = data['author_id']
#         content = data['content']
#         post = PostRepository.create_post(post_repo, thread_id, author_id, content)
#         return jsonify(post), 201
#     except ValueError as e:
#         return jsonify({'error': str(e)}), 404
#     except Exception as e:
#         print('thread_routes.py')
#         return jsonify({'error': str(e)}), 500


        