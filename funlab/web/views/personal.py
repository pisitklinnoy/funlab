import datetime
import mongoengine as me
import requests
from PIL import Image
from io import BytesIO

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
import os

module = Blueprint("personal", __name__, url_prefix="/personal")


@module.route("/", methods=["GET", "POST"])
def index():
    form = forms.PersonalForm()
    if not form.validate_on_submit():
        print(form.errors)
        return render_template("/personal/index.html", form=form)
    personal = models.Personal()
    form.populate_obj(personal)
    if form.document_upload.data:
        print("img_data", form.document_upload.data)
        if not personal.file:
            personal.file.put(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )
        else:
            personal.file.replace(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )

    personal.save()
    return redirect(url_for("home.show_info"))


@module.route("/<personal_id>/calculator", methods=["GET", "POST"])
def calculator(personal_id):
    personal = models.Personal.objects(id=personal_id).first()
    image_path = "http://localhost:8080" + url_for(
        "foodimage.get_image", document_id=personal.id, filename="uu"
    )
    response = requests.get(image_path)

    # Step 2: Check if the request was successful
    if response.status_code == 200:
        # Step 3: Open the image from the response content
        image = Image.open(BytesIO(response.content))

        # Step 4: Display or process the image (Optional)
        image.show()  # Opens the image using the default viewer

        # If you want to save the image locally
        image.save(
            "/home/beer/project/funlab/funlab/web/views/utils/temp/downloaded_image.jpg"
        )
    else:
        print(f"Failed to fetch image. Status code: {response.status_code}")
    results = main(
        weight=personal.weight,
        height=personal.height,
        age=personal.age,
        sex=personal.gender,
        activity=personal.activity,
        image_path="/home/beer/project/funlab/funlab/web/views/utils/temp/downloaded_image.jpg",
        image_name="downloaded_image.jpg",
        # image_name=personal.file.filename,
    )
    print("result = ", results)
    image_path = get_latest_exp_file()
    print(image_path)

    return render_template(
        "/personal/calculator.html",
        personal=personal,
        results=results,
        image_path=image_path,
    )


# แคลที่ต้องใช้
def calculatecaloriesforday(weight, height, age, sex, activity):
    if sex == "male":
        BMR = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
    elif sex == "female":
        BMR = 665 + (9.6 * weight) + (1.8 * height) - (4.7 * age)
    if activity == "นั่งทำงานอยู่กับที่ และไม่ได้ออกกำลังกายเลย":
        TDFF = BMR * 1.2
    elif activity == "ออกกำลังกายหรือเล่นกีฬาเล็กน้อย ประมาณอาทิตย์ละ 1-3 วัน":
        TDFF = BMR * 1.375
    elif activity == "ออกกำลังกายหรือเล่นกีฬาปานกลาง ประมาณอาทิตย์ละ 3-5 วัน":
        TDFF = BMR * 1.55
    elif activity == "ออกกำลังกายหรือเล่นกีฬาอย่างหนัก ประมาณอาทิตย์ละ 6-7 วัน":
        TDFF = BMR * 1.725
    elif activity == "ออกกำลังกายหรือเล่นกีฬาอย่างหนักทุกวันเช้าเย็น":
        TDFF = BMR * 1.9
    return TDFF


# แคลอรี่ของอาหารแต่ละชนิดต่อจาน
def calculatetotalcalories(listfood):  # [9,9,9,8]
    print(listfood)
    number_of_food = {
        "0": "French-fries",
        "1": "KFC",
        "2": "burger",
        "3": "cake",
        "4": "hot-dog",
        "5": "pizza",
        "6": "salad",
        "12": "spaghetti",
        "8": "steak",
        "9": "sushi",
    }
    calorie_info = {
        "French-fries": 200,
        "KFC": 250,
        "burger": 150,
        "cake": 100,
        "hot-dog": 100,
        "pizza": 100,
        "salad": 100,
        "spaghetti": 150,
        "steak": 100,
        "sushi": 100,
    }
    listcal = []
    for i in listfood:
        i = str(i)
        foodtype = number_of_food[i]
        calorieforone = calorie_info[foodtype]
        listcal.append(calorieforone)
    totalcal = sum(listcal)
    return totalcal


def get_latest_exp_folder():
    runs_dir = "funlab/web/views/utils/runs/detect"

    subdirs = [
        d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))
    ]
    # ค้นหาโฟลเดอร์ล่าสุดที่เริ่มต้นด้วย 'exp'
    exp_dirs = sorted(
        [d for d in subdirs if d.startswith("exp")],
        key=lambda x: os.path.getmtime(os.path.join(runs_dir, x)),
        reverse=True,
    )

    if exp_dirs:
        return os.path.join(runs_dir, exp_dirs[0])  # คืนค่าโฟลเดอร์ 'exp' ล่าสุด
    return None


def read_latest_class_indices(image_name):
    latest_exp_folder = get_latest_exp_folder()  # ค้นหาโฟลเดอร์ 'exp' ล่าสุด
    print(f"Last Folder {latest_exp_folder}")
    class_indices = []
    if latest_exp_folder:
        # ค้นหาไฟล์ .txt ที่ตรงกับชื่อภาพในโฟลเดอร์ labels
        results_file = os.path.join(
            latest_exp_folder, "labels", image_name.replace(".jpg", ".txt")
        )
        print(f"{results_file}")
        print("Do Code")
        if os.path.exists(results_file):
            with open(results_file, "r") as f:
                lines = f.readlines()
                print(f"##### Line {lines}")
                for line in lines:
                    class_index = int(line.split()[0])  # ดึงค่า class_index จากแต่ละบรรทัด
                    class_indices.append(class_index)  # เก็บค่า class_index ใน list
    return class_indices


# print(calculatetotalcalories(read_latest_class_indices('IMG_20241004_200105.jpg')))
def predict_image(image_path):
    weights = "/home/beer/project/funlab/funlab/web/views/utils/models/best.pt"
    img_size = 224
    conf_thresh = 0.25
    data_yaml = "/home/beer/project/funlab/Training/data/data.yaml"
    yolov5_path = "/home/beer/project/funlab/Training/detect.py"

    command = (
        f"python3 {yolov5_path} --weights {weights} --img {img_size} --conf {conf_thresh} --project /home/beer/project/funlab/funlab/web/views/utils/runs/detect"
        + f" --source {image_path} --data {data_yaml} --save-txt"
    )
    print(f"Run Command : {command}")
    result = os.system(command)
    print(f"This command {result}")


# image_path = "/home/beer/images/pizzaforai.jpg"
# weight=int(input("weight :"))
# height=int(input("height :"))
# age=int(input("age :"))
# sex=str(input("sex :"))
# activity="ออกกำลังกายหรือเล่นกีฬาอย่างหนักทุกวันเช้าเย็น"
# image_name='pizzaforai.jpg'

import os


def get_latest_exp_file():
    runs_dir = "funlab/web/views/utils/runs/detect"

    # ค้นหาโฟลเดอร์ที่อยู่ใน runs_dir และเป็นโฟลเดอร์จริง ๆ
    subdirs = [
        d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))
    ]

    # ค้นหาโฟลเดอร์ล่าสุดที่เริ่มต้นด้วย 'exp'
    exp_dirs = sorted(
        [d for d in subdirs if d.startswith("exp")],
        key=lambda x: os.path.getmtime(os.path.join(runs_dir, x)),
        reverse=True,
    )

    if exp_dirs:
        latest_exp_dir = os.path.join(runs_dir, exp_dirs[0])
        image_path = os.path.join(
            latest_exp_dir,
        )

        # ตรวจสอบว่าไฟล์มีอยู่จริง
        if os.path.exists(image_path):
            return image_path
        else:
            return "ไม่พบไฟล์ downloaded_image.jpg ในโฟลเดอร์ล่าสุด"
    else:
        return "ไม่พบโฟลเดอร์ที่เริ่มต้นด้วย 'exp' ใน runs_dir"


# เรียกใช้ฟังก์ชัน
latest_image = get_latest_exp_file()
print("--------------------------------------------------", latest_image)


def main(weight, height, age, sex, activity, image_path, image_name):
    predict_image(image_path)
    totalcal = calculatetotalcalories(read_latest_class_indices(image_name))
    needscal = calculatecaloriesforday(weight, height, age, sex, activity)
    # print(F'Foods_with {totalcal} calories.')
    # print(F'Total Daily Energy Expenditure is {needscal:.2f} calories.')
    return f"Foods_with {totalcal} calories.\nTotal Daily Energy Expenditure is {needscal:.2f} calories."


# print(main(weight,height,age,sex,activity,image_path,image_name))


# "C:\Users\teera\Downloads\kfc.jpg"
# "C:\Users\teera\Downloads\archive\images\hamburger\1567823.jpg"

# import tkinter as tk
# from tkinter import filedialog
#    # สร้างหน้าต่างเลือกไฟล์
# root = tk.Tk()
# root.withdraw()  # ซ่อนหน้าต่างหลักของ tkinter

# # เปิดหน้าต่างให้ผู้ใช้เลือกไฟล์ .jpg
# file_path = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])

# แยกชื่อไฟล์จาก path
# file_name = os.path.basename(file_path)  # วิธีที่ 1: ใช้ os.path

# predict_image("C:/Users/teera/Downloads/kfc.jpg")
