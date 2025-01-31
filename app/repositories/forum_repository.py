from app.database.rdbms import Forum
from app.database.rdbms import Thread
from app.repositories.thread_repository import ThreadRepository
from app import db
from flask import Flask, render_template, request, redirect, url_for


class ForumRepository:
    @staticmethod
    def create_forum(name, description):
        new_forum = Forum(name=name, description=description)
        db.session.add(new_forum)
        db.session.commit()
        return new_forum

    @staticmethod
    def get_forum_by_id(forum_id):
        return Forum.query.get(forum_id)

    @staticmethod
    def get_all_forums():
        return Forum.query.all()

    @staticmethod
    def update_forum(forum_id, name, description):
        forum = Forum.query.get(forum_id)
        forum.name = name
        forum.description = description
        db.session.commit()
        return forum

    @staticmethod
    def delete_forum(forum_id):
        forum = Forum.query.get(forum_id)
        
        # delete the threads
        threads = Thread.query.filter_by(forum_id=forum_id).all()
        for thread in threads:
            ThreadRepository.delete_thread(thread.id)
        db.session.delete(forum)
        db.session.commit()
        return forum
