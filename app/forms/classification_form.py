from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, BooleanField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired

from wtforms import BooleanField

from app.utils.list_images import list_images
from config import Configuration

conf = Configuration()


class ClassificationForm(FlaskForm):
    """
    Form for selecting a model and an image and running a classification job.
    model: the model to use for classification
    image: the image to classify
    upload_file: the file to upload
    use_own_img: whether to use the uploaded file or not
    """
    model = SelectField('model', choices=conf.models, validators=[DataRequired()])
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    upload_file = FileField(id='upload_file')
    use_own_img = BooleanField(id='use_own_img_cbx')
    submit = SubmitField('Submit')
