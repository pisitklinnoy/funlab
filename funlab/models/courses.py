import mongoengine as me
import datetime

COURSE_STATUS = [
    ("pending", "รอดําเนินการ"),
    ("active", "เปิดใช้งาน"),
    ("disactive", "ปิดใช้งาน"),
]


class Course(me.Document):
    meta = {"collection": "courses"}

    name = me.StringField(max_length=256, required=True)
    description = me.StringField()

    professor = me.ReferenceField("User", dbref=True)

    code = me.StringField(max_length=128, required=True)
    enrollment = me.IntField(min_value=0, max_value=1000)

    status = me.StringField(default="pending", choices=COURSE_STATUS)

    creator = me.ReferenceField("User", dbref=True)
    updater = me.ReferenceField("User", dbref=True)

    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(required=True, default=datetime.datetime.now)
