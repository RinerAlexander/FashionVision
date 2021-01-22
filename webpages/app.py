import os

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    send_from_directory)

import numpy as np
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras.models import load_model

from werkzeug.utils import secure_filename


app = Flask(__name__)

model = load_model ("filename2.h5")

@app.route("/", methods=["GET", "POST"])
def upload_picture():

    if request.method == "POST":
        print("first")

        picture = request.files["image"]
        picture.save("input.jpg")

        im = image.load_img("input.jpg", target_size=(28,28), color_mode="grayscale")
        pixel_array = img_to_array(im)
        pixel_array /= 255
        answer=model.predict_classes(pixel_array)

        return render_template("file_upload_test.html",picture="input",message=answer)
        

    return render_template("file_upload_test.html")

@app.route("/input")
def input():
    return send_from_directory("","input.jpg")

if __name__ == "__main__":
    app.run(debug=True)