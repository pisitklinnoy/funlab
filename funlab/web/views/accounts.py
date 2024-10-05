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

from funlab.models import users
from .. import oauth2
from .. import acl
from .. import forms

module = Blueprint("accounts", __name__)


@module.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if not form.validate_on_submit():
        error_msg = form.errors
        print(form.errors)
        return render_template("accounts/login.html", form=form)

    user = users.User.objects(username=form.username.data).first()

    if not user or not user.check_password(form.password.data):
        print(form.errors)
        error_msg = "โปรดตรวจสอบ username และ password ของท่าน"
        return render_template("accounts/login.html", form=form, error_msg=error_msg)

    if user.status == "disactive":
        print(form.errors)
        error_msg = "username ของท่านถูกลบออกจากระบบ"
        return render_template("accounts/login.html", form=form, error_msg=error_msg)

    login_user(user)
    user.last_login_date = datetime.datetime.now()
    user.save()
    next = request.args.get("next")
    if next:
        return redirect(next)

    return redirect(url_for("site.index"))


@module.route("/register", methods=["GET", "POST"])
def register():
    form = forms.accounts.RegisterForm()
    if not form.validate_on_submit():
        return render_template("accounts/register.html", form=form)
    user = users.User.objects(username=form.username.data)
    if user:
        error_msg = "Username นี้ถูกใช้งานแล้ว"
        return render_template("accounts/register.html", form=form, error_msg=error_msg)
    user = users.User.objects(email=form.email.data)
    if user:
        error_msg = "Email นี้ถูกใช้งานแล้ว"
        return render_template("accounts/register.html", form=form, error_msg=error_msg)
    user = users.User()
    form.populate_obj(user)
    user.set_password(form.input_password.data)
    user.save()
    return redirect(url_for("accounts.login", messages="success"))


@module.route("/login/<name>")
def login_oauth(name):
    client = oauth2.oauth2_client

    scheme = request.environ.get("HTTP_X_FORWARDED_PROTO", "http")
    redirect_uri = url_for(
        "accounts.authorized_oauth", name=name, _external=True, _scheme=scheme
    )
    response = None
    if name == "google":
        response = client.google.authorize_redirect(redirect_uri)
    elif name == "facebook":
        response = client.facebook.authorize_redirect(redirect_uri)
    elif name == "line":
        response = client.line.authorize_redirect(redirect_uri)

    elif name == "psu":
        response = client.psu.authorize_redirect(redirect_uri)
    elif name == "engpsu":
        response = client.engpsu.authorize_redirect(redirect_uri)
    return response


@module.route("/auth/<name>")
def authorized_oauth(name):
    client = oauth2.oauth2_client
    remote = None
    try:
        if name == "google":
            remote = client.google
        elif name == "facebook":
            remote = client.facebook
        elif name == "line":
            remote = client.line
        elif name == "psu":
            remote = client.psu
        elif name == "engpsu":
            remote = client.engpsu

        token = remote.authorize_access_token()

    except Exception as e:
        print("autorize access error =>", e)
        return redirect(url_for("accounts.login"))

    session["oauth_provider"] = name
    return oauth2.handle_authorized_oauth2(remote, token)


@module.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("site.index"))