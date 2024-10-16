from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from funlab import models

BaseImageForm = model_form(
    models.FoodImage,
    FlaskForm,
    exclude=[
        "created_date",
        "updated_date",
        "document",
    ],
    field_args={
        "document": {"label": "Upload file"},
    },
)


class FoodImageForm(BaseImageForm):
    document_upload = FileField(
        "Upload image",
        validators=[
            FileAllowed(
                ["png", "jpg", "bmp", "webp", "tiff"], "only JPG, PNG, bmp, webp, tiff"
            )
        ],
    )
