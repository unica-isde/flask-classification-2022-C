from flask import render_template
from app import app, config
from app.forms.histogram_form import HistogramForm
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2


@app.route('/histogram', methods=['GET', 'POST'])
def histogram():
    form = HistogramForm()
    if form.validate_on_submit():
        image_id = form.image.data

        path = os.path.join(config.image_folder_path, image_id)
        path_histograms = os.path.join(config.histogram_folder_path, image_id)

        if not os.path.exists(config.histogram_folder_path):
            os.mkdir(config.histogram_folder_path)

        image = cv2.imread(path)
        vals = image.mean(axis=2).flatten()
        # calculate histogram
        plt.figure()

        counts, bins = np.histogram(vals, range(257))
        # plot histogram centered on values 0..255

        plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
        plt.xlim([-0.5, 255.5])
        plt.title("Histogram")
        plt.xlabel("Value")
        plt.ylabel("Pixel count")

        plt.savefig(path_histograms)
        plt.close()
        return render_template('histogram_output.html', image_id=image_id)
    return render_template('histogram_select.html',
                           form=form)
