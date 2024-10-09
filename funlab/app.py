from flask import Flask, render_template
import shutil
import os

app = Flask(__name__)


@app.route("/calculator")
def calculator():
    # คัดลอกไฟล์จาก exp84 ไปยัง static
    src = "funlab/web/views/utils/runs/detect/exp84/downloaded_image.jpg"
    dest = "static/downloaded_image.jpg"

    # ตรวจสอบว่ามีไฟล์ต้นฉบับอยู่หรือไม่
    if os.path.exists(src):
        shutil.copy(src, dest)
        print("Image copied successfully!")
    else:
        print("Source image does not exist.")

    # URL ของภาพที่อยู่ใน static
    image_url = "downloaded_image.jpg"

    return render_template("personal/calculator.html", image_url=image_url)


if __name__ == "__main__":
    app.run(debug=True)
