import os
from PIL import Image
from flask import render_template
from app import app
from app.forms.transformation_form import TransformationForm
from config import Configuration
from werkzeug.utils import secure_filename
from PIL import ImageEnhance

config = Configuration()


@app.route('/transformation', methods=['GET', 'POST'])
def transformation():
    """
        App route which manage operations on image transformation.

        :return: The template with base and transformed images.
        :rtype: str

        """
    form = TransformationForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        uploaded_file = form.upload_file.data
        use_own_img = form.use_own_img.data
        color = form.color.data
        contrast = form.contrast.data
        brightness = form.brightness.data
        sharpness = form.sharpness.data

        if use_own_img:
            # user want to use his own image
            if uploaded_file:
                # user uploaded a file
                image_to_process = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(config.image_folder_path, image_to_process))
            else:
                # user did not upload a file
                image_to_process = None
        else:
            # user wants to use one of the default images
            image_to_process = image_id

        new_image = Image.open(os.path.join(config.image_folder_path, image_to_process))
        new_image = ImageEnhance.Color(new_image).enhance(color)
        new_image = ImageEnhance.Contrast(new_image).enhance(contrast)
        new_image = ImageEnhance.Brightness(new_image).enhance(brightness)
        new_image = ImageEnhance.Sharpness(new_image).enhance(sharpness)
        image_to_process_edited = "image_to_process_edited"
        new_image.save(os.path.join(config.image_folder_path, image_to_process_edited), format='PNG')

        # returns the image classification output from the specified model
        return render_template("transformation_output.html", old_image=image_to_process, new_image=image_to_process_edited)

    # otherwise, it is a get request and should return the transformation selection
    return render_template('transformation_select.html', form=form)
