import mongoengine as me
import datetime

GENDER = [("male", "Male"), ("female", "Female")]


class Personal(me.Document):
    meta = {"collection": "personals"}
    first_name = me.StringField(required=True, max_length=255)
    last_name = me.StringField(required=True, max_length=255)

    weight = me.FloatField(required=True, min_value=0)
    height = me.FloatField(required=True, min_value=0)
    gender = me.StringField(required=True, choices=GENDER)
    age = me.IntField(required=True, min_value=0)

    created_date = me.DateTimeField(default=datetime.datetime.now)
    updated_date = me.DateTimeField(default=datetime.datetime.now)
