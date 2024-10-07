from flask import Blueprint, render_template
from  funlab.web  import models

module = Blueprint("home", __name__, url_prefix="/food")


@module.route("/", methods=["GET", "POST"])
def index():
    
    return render_template(
        "home/index.html",
    )

@module.route("/show_info", methods=["GET", "POST"])
def show_info():
    info = models.Personal.objects()
    return render_template(
        "home/show_info.html",info=info 
    )