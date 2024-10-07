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

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    Response,
    request,
    send_from_directory,
)
from flask_login import login_required
import os
import datetime
import imageio
import mimetypes

module = Blueprint("foodimage", __name__, url_prefix="/foodimage")

# โฟลเดอร์สำหรับเก็บรูปภาพ
UPLOAD_FOLDER = "static/uploads/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# เก็บข้อมูลรูปภาพใน list แทน MongoDB
food_images = []


@module.route("/")
@login_required
def index():
    # ส่งข้อมูลรูปภาพไปยัง template
    return render_template("foodimage/index.html", foodimages=food_images)


@module.route("/<document_id>/picture/<filename>")
def get_image(document_id, filename):
    print(filename)
    personal = models.Personal.objects(id=document_id).first()

    # img = imageio.imread(f"static/uploads/{filename}")
    # mime_type, _ = mimetypes.guess_type(filename)
    # print("#########")
    response = send_file(
        personal.file,
        download_name=personal.file.filename,
        mimetype=personal.file.content_type,
    )

    return response


@module.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = forms.foodimages.FoodImageForm()

    if request.method == "POST" and form.validate_on_submit():
        file = request.files.get("document_upload")

        if file:
            # เซฟไฟล์ลงในโฟลเดอร์
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # เพิ่มข้อมูลรูปภาพลงในตัวแปร list
            food_image = {
                "id": len(food_images) + 1,
                "path": file_path,
                "created_date": datetime.datetime.now(),
                "updated_date": datetime.datetime.now(),
                "filename": filename,
            }
            food_images.append(food_image)
            print(food_image)

            return redirect(url_for("foodimage.index"))

    return render_template("foodimage/foodimage-create-edit.html", form=form)


@module.route("/<foodimage_id>/delete", methods=["POST"])
@login_required
def delete(foodimage_id):
    # ลบรูปภาพจาก list และไฟล์จากโฟลเดอร์
    global food_images
    food_images = [img for img in food_images if str(img["id"]) != foodimage_id]
    return redirect(url_for("foodimage.index"))


@module.route("/<foodimage_id>/edit", methods=["GET", "POST"])
@login_required
def edit(foodimage_id):
    foodimage = next(
        (img for img in food_images if str(img["id"]) == foodimage_id), None
    )
    form = forms.foodimages.FoodImageForm(obj=foodimage)

    if request.method == "POST" and form.validate_on_submit():
        file = request.files.get("document_upload")
        if file:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            foodimage["name"] = filename
            foodimage["path"] = file_path

        foodimage["updated_date"] = datetime.datetime.now()
        return redirect(url_for("foodimage.index"))

    return render_template(
        "foodimage/foodimage-create-edit.html", form=form, foodimage=foodimage
    )
