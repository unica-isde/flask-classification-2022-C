import os
import redis
from flask import render_template
from rq import Connection, Queue
from rq.job import Job
from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import classify_image
from config import Configuration
from werkzeug.utils import secure_filename
import time

config = Configuration()


@app.route('/classifications', methods=['GET', 'POST'])
def classifications():
    """API for selecting a model and an image and running a 
    classification job. Returns the output scores from the 
    model."""

    form = ClassificationForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        model_id = form.model.data
        uploaded_file = form.upload_file.data
        use_own_img = form.use_own_img.data

        if use_own_img:
            # user want to use his own image
            if uploaded_file:
                # user uploaded a file
                image_to_process = 'UPL_' + str(time.time()) + '_' + secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(config.image_folder_path, image_to_process))
            else:
                # user did not upload a file
                image_to_process = None
        else:
            # user wants to use one of the default images
            image_to_process = image_id

        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": model_id,
                "img_id": image_to_process
            })
            task = q.enqueue_job(job)

        # returns the image classification output from the specified model
        return render_template("classification_output_queue.html", image_id=image_to_process, jobID=task.get_id())

    # otherwise, it is a get request and should return the
    # image and model selector
    return render_template('classification_select.html', form=form)
