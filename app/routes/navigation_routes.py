from flask import Blueprint, request, jsonify
from openai import OpenAI
from app.utils.auth import token_required
from app.database.pinecone import index 
import os
from flask import Flask, render_template, request, redirect, url_for
from app.database.rdbms import db, Forum, Thread
from app import mongo
from app.repositories.post_repository import PostRepository
from app.repositories.thread_repository import ThreadRepository
from app.repositories.forum_repository import ForumRepository

func_bp = Blueprint('func', __name__)

@func_bp.route('/', methods=['GET'])  # create
# @token_required
def render_home():
    forums = Forum.query.all()
    return render_template('index.html', forums=forums)


# @func_bp.route('/forum/<int:forum_id>')
# def view_forum(forum_id):
#     forum = Forum.query.get(forum_id)
#     threads = Thread.query.filter_by(forum_id=forum.id).all()
#     return render_template('forum.html', forum=forum, threads=threads)

# @func_bp.route('/forum/<int:forum_id>/thread/<int:thread_id>')
# def view_thread(forum_id, thread_id):
#     forum = Forum.query.get(forum_id)
#     thread = Thread.query.get(thread_id)
#     posts = PostRepository.get_posts_by_thread(thread_id)
#     return render_template('thread.html', forum=forum, thread=thread, posts=posts)

# @func_bp.route('/create_forum', methods=['GET', 'POST'])
# def create_forum():
#     if request.method == 'POST':
#         name = request.form['name']
#         description = request.form['description']
#         ForumRepository.create_forum(name, description) # only moderators can do it
#         return redirect(url_for('index'))
#     return render_template('create_forum.html')

# @func_bp.route('/forum/<int:forum_id>/create_thread', methods=['GET', 'POST'])
# def create_thread(forum_id):
#     forum = Forum.query.get(forum_id)
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         new_thread = Thread(title=title, forum_id=forum.id)
#         db.session.add(new_thread)
#         db.session.commit()
#         new_post = Post(content=content, thread_id=new_thread.id)
#         db.session.add(new_post)
#         db.session.commit()
#         return redirect(url_for('view_forum', forum_id=forum.id))
#     return render_template('create_thread.html', forum=forum)

# @func_bp.route('/forum/<int:forum_id>/thread/<int:thread_id>/create_post', methods=['POST'])
# def create_post(forum_id, thread_id):
#     content = request.form['content']
#     new_post = Post(content=content, thread_id=thread_id)
#     db.session.add(new_post)
#     db.session.commit()
#     return redirect(url_for('view_thread', forum_id=forum_id, thread_id=thread_id))
