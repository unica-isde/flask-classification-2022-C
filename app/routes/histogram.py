from flask import render_template
from app import app, config
from app.forms.histogram_form import HistogramForm
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import time

@app.route('/histogram', methods=['GET', 'POST'])
def histogram():
    """
        Returns the histogram plot of a given image.

        :param kind: Optional "kind" of ingredients.
        :type kind: list[str] or None
        :raise lumache.InvalidKindError: If the kind is invalid.
        :return: The ingredients list.
        :rtype: list[str]

    """
    form = HistogramForm()
    if form.validate_on_submit():
        image_id = form.image.data
        image_histogram_id = 'H_' + str(time.time()) + '_' + image_id

        path = os.path.join(config.image_folder_path, image_id)
        path_histograms = os.path.join(config.image_folder_path, image_histogram_id)

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
        return render_template('histogram_output.html', image_id=image_id, histogram_id=image_histogram_id)
    return render_template('histogram_select.html',
                           form=form)
