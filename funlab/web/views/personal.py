import datetime
import mongoengine as me

from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    request,
    session,
    current_app,
    send_file,
    abort,
)
from flask_login import login_user, logout_user, login_required, current_user

from funlab import models
from .. import oauth2
from .. import acl
from .. import forms

module = Blueprint("personal", __name__, url_prefix="/personal")


@module.route("/", methods=["GET", "POST"])
def index():
    form = forms.PersonalForm()
    if not form.validate_on_submit():
        print(form.errors)
        return render_template("/personal/index.html", form=form)
    personal = models.Personal()
    form.populate_obj(personal)
    personal.save()
    return redirect(url_for("home.index"))
