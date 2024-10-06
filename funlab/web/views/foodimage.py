from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    Response,
    send_file,
    request,
)
from flask_login import login_required, current_user

from funlab.web import models, forms, acl

import datetime

module = Blueprint("foodimage", __name__, url_prefix="/foodimage")


@module.route("/")
@login_required
def index():
    foodimages = models.FoodImage.objects()
    return render_template(
        "foodimage/index.html",
        foodimages=foodimages,
    )


@module.route("/<document_id>/picture/<filename>")
def get_image(document_id, filename):
    response = Response()
    response.status_code = 404

    foodimage = models.FoodImage.objects(id=document_id).first()
    response = foodimage.get_picture()
    return response


@module.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = forms.foodimages.FoodImageForm()
    foodimages = models.FoodImage()

    if not form.validate_on_submit():
        print(form.errors)
        return render_template(
            "foodimage/foodimage-create-edit.html",
            form=form,
        )

    form.populate_obj(foodimages)

    if form.document_upload.data:
        print("img_data", form.document_upload.data)
        if not foodimages.document:
            foodimages.document.put(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )
        else:
            foodimages.document.replace(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )

    foodimages.save()

    return redirect(url_for("foodimage.index"))


@module.route("/<foodimage_id>/delete", methods=["GET", "POST"])
@login_required
def delete(foodimage_id):
    foodimage = models.FoodImage.objects.get(id=foodimage_id)

    foodimage.delete()

    return redirect(url_for("foodimage.index"))


@module.route("/<foodimage_id>/edit", methods=["GET", "POST"])
@login_required
def edit(foodimage_id):
    foodimage = models.FoodImage.objects.get(id=foodimage_id)
    form = forms.foodimages.FoodImageForm(obj=foodimage)
    if not form.validate_on_submit():
        return render_template(
            "foodimage/foodimage-create-edit.html",
            form=form,
            foodimage=foodimage,
        )

    form.populate_obj(foodimage)
    if form.document_upload.data:
        print("img_data", form.document_upload.data)
        if not foodimage.document:
            foodimage.document.put(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )
        else:
            foodimage.document.replace(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )

    foodimage.updated_date = datetime.datetime.now()
    foodimage.save()

    return redirect(url_for("foodimage.index"))
