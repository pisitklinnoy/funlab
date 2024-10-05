from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user


module = Blueprint("foods", __name__, url_prefix="/foods")


@module.route("/")
def index():
    return render_template("foods/index.html")
