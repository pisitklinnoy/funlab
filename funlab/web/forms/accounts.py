from flask_wtf import FlaskForm
from wtforms import fields, validators

from flask_wtf.file import FileAllowed
from flask_mongoengine.wtf import model_form
from funlab import models


class RegisterForm(FlaskForm):
    username = fields.StringField(
        "Username",
        [
            validators.DataRequired("Username is required."),
            validators.Length(min=1),
        ],
    )
    input_password = fields.PasswordField(
        "รหัสผ่าน",
        validators=[
            validators.InputRequired(),
            validators.Length(min=6),
        ],
        render_kw={"placeholder": "รหัสผ่าน", "autocomplete": "new-password"},
    )
    confirm_password = fields.PasswordField(
        "ยืนยันรหัสผ่าน",
        validators=[
            validators.InputRequired(),
            validators.Length(min=6),
            validators.EqualTo("input_password", message="รหัสผ่านไม่ตรงกัน"),
        ],
        render_kw={"placeholder": "ยืนยันรหัสผ่าน", "autocomplete": "new-password"},
    )
    email = fields.EmailField(
        "Email",
        validators=[validators.InputRequired()],
        render_kw={
            "placeholder": "อีเมล",
        },
    )

class LoginForm(FlaskForm):
    username = fields.StringField(
        "Username",
        [
            validators.DataRequired("Username is required."),
            validators.Length(min=1),
        ],
    )
    password = fields.PasswordField(
        "Password", [validators.DataRequired("Password is required.")]
    )
    submit = fields.SubmitField("Login")
