import datetime

import mongoengine as me
from flask import url_for, send_file


class FoodImage(me.Document):
    meta = {"collection": "committee"}
    document = me.FileField(required=True)
    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(required=True, default=datetime.datetime.now)

    def get_picture(self):
        if self.document:
            response = send_file(
                self.document,
                download_name=self.document.filename,
                mimetype=self.document.content_type,
            )
            return response
        else:
            pass
