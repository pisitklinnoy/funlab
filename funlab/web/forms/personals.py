from flask_wtf import FlaskForm
from wtforms import fields, validators

from flask_wtf.file import FileAllowed
from flask_mongoengine.wtf import model_form
from funlab import models

BasePersonalForm = model_form(
    models.Personal,
    FlaskForm,
    exclude=["created_date", "updated_date"],
    field_args={
        "first_name": {"label": "First Name"},
        "last_name": {"label": "Last Name"},
        "weight": {"label": "Weight"},
        "height": {"label": "Height"},
    },
)


class PersonalForm(BasePersonalForm):
    gender = fields.SelectField("Gender", choices=models.personals.GENDER)
