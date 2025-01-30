from app import db
from app.repositories.forum_repository import ForumRepository
from app.repositories.thread_repository import ThreadRepository
from app.repositories.post_repository import PostRepository
from faker import Faker
from datetime import datetime
import pytz
from app import create_app

# Initialize Faker instance
fake = Faker()

def generate_fake_forum():

    forum = ForumRepository.create_forum(fake.word(), fake.sentence())  # Use repository to create and return the forum
    return forum

def generate_fake_thread(forum):
    # Generate fake thread data using the ThreadRepository
    thread = ThreadRepository.create_thread(fake.sentence(), forum.id, 1)  # Use repository to create and return the thread
    return thread

def generate_fake_post(thread):
  
    post = PostRepository.create_post(fake.text(), thread.id, 1)  # Use repository to create and return the post
    return post

def generate_fake_data(num_forums=5, threads_per_forum=3, posts_per_thread=10):
    # Generate a certain number of fake forums, threads, and posts
    for _ in range(num_forums):
        forum = generate_fake_forum()  # Create a forum
        for _ in range(threads_per_forum):
            thread = generate_fake_thread(forum)  # Create a thread for the forum
            for _ in range(posts_per_thread):
                generate_fake_post(thread)  # Create posts within the thread

    print(f"Generated {num_forums} forums with {threads_per_forum} threads each, and {posts_per_thread} posts per thread.")

if __name__ == "__main__":
    app = create_app()  # Create the Flask app
    with app.app_context():  # Ensure app context is active
        generate_fake_data()
