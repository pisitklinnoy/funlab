from flask_wtf import FlaskForm
from wtforms import PasswordField, validators,StringField,SelectField
from flask_mongoengine.wtf import model_form
from funlab.web import models




BaseLoginForm = model_form(
   models.User,
   FlaskForm,
   field_args={"username" : {"label" : "Username"}},
   only=["username","password"],
)


class LoginForm(BaseLoginForm):
   password = PasswordField("Password",validators=[validators.InputRequired(),validators.Length(min=6)])