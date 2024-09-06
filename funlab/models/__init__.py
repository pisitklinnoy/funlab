import mongoengine as me
from flask_mongoengine import MongoEngine


__all__ = []


db = MongoEngine()


def init_db(app):
   db.init_app(app)
