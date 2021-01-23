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

model = load_model ("EPOCH60ver2.h5")
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

@app.route("/", methods=["GET", "POST"])
def upload_picture():

    if request.method == "POST":
        print("first")

        picture = request.files["image"]
        file_name=picture.filename
        picture.save(file_name)
        
        im = image.load_img(file_name, target_size=(28,28), color_mode="grayscale")
        pixel_array = img_to_array(im)

        for row in pixel_array:
            for pixel in row:
                if pixel[0]>=235:
                    pixel[0]=0
        
        pixel_array /= 255

        pixel_array = np.expand_dims(pixel_array, axis = 0)
        
        answer=model.predict_classes(pixel_array)[0]
        answer=class_names[answer]

        return render_template("file_upload_test.html",picture=f"input/{file_name}",message=answer)
        

    return render_template("file_upload_test.html")

@app.route("/input/<file>")
def input(file):
    return send_from_directory("",f"{file}")

if __name__ == "__main__":
    app.run(debug=True)