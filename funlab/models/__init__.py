import mongoengine as me
from flask_mongoengine import MongoEngine

from .users import User
from .personals import Personal
from .courses import Course
from .organizations import Organization


__all__ = ["User","Organization","Personal","Course"]


db = MongoEngine()


def init_db(app):
   db.init_app(app)
