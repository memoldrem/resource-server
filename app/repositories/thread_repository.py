from datetime import datetime
import pytz
from app.database.rdbms import Thread
from app import db
from app.repositories.post_repository import PostRepository 
from app import mongo

class ThreadRepository:
    @staticmethod
    def create_thread(title: str, forum_id: int, author_id: int) -> Thread:
        new_thread = Thread(title=title, post_count=0, forum_id=forum_id, author_id=author_id, last_post_at=datetime.now(pytz.UTC))
        db.session.add(new_thread)
        db.session.commit()
        return new_thread

    @staticmethod
    def get_thread_by_id(thread_id: int) -> Thread:
        thread = Thread.query.get(thread_id)
        if thread is None:
            raise ValueError(f"Thread with ID {thread_id} not found")
        return thread

    @staticmethod
    def get_threads_by_forum(forum_id: int) -> list[Thread]:
        return Thread.query.filter_by(forum_id=forum_id).all()

    @staticmethod
    def get_threads_by_author(author_id: int) -> list[Thread]:
        return Thread.query.filter_by(author_id=author_id).all()

    @staticmethod
    def delete_thread(post_repo: PostRepository, thread_id: int) -> str:
        thread = Thread.query.get(thread_id)
        if thread is None:
            raise ValueError(f"Thread with ID {thread_id} not found")
        # delete all posts in thread
        post_repo.delete_posts_by_thread(thread_id)
        db.session.delete(thread)
        db.session.commit()
        return f"Thread with ID {thread_id} has been deleted successfully"
