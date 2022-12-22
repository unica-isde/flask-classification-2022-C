from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField, FloatField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired

from wtforms import BooleanField

from app.utils.list_images import list_images


class TransformationForm(FlaskForm):
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    upload_file = FileField(id='upload_file')
    use_own_img = BooleanField(id='use_own_img_cbx')
    color = FloatField(label="Select color enhancer (Min 0, Default and Max: 1)", default=1)
    contrast = FloatField(label="Select contrast enhancer (Min 0, Default and Max: 1)", default=1)
    brightness = FloatField(label="Select brightness enhancer (Min 0, Default and Max: 1)", default=1)
    sharpness = FloatField(label="Select sharpness enhancer (Min 0, Default 1, Max: 2)", default=1)

    # Transformation form
    submit = SubmitField('Submit')
