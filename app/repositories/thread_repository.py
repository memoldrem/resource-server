from app.database.rdbms import Thread
from app import db

class ThreadRepository:
    @staticmethod
    def create_thread(title, content, forum_id):
        new_thread = Thread(title=title, content=content, forum_id=forum_id)
        db.session.add(new_thread)
        db.session.commit()
        return new_thread

    @staticmethod
    def get_thread_by_id(thread_id):
        return Thread.query.get(thread_id)

    @staticmethod
    def get_threads_by_forum(forum_id):
        return Thread.query.filter_by(forum_id=forum_id).all()