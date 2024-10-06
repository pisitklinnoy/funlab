import mongoengine as me
from flask_mongoengine import MongoEngine

from .users import User
from .personals import Personal
from .courses import Course
from .foodimages import FoodImage

__all__ = ["User", "Personal", "Course", "FoodImage"]


db = MongoEngine()


def init_db(app):
    db.init_app(app)
