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

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/imageUpload", methods=["GET", "POST"])
def imageUpload():

    if request.method == "POST":
        print("first")

        picture = request.files["image"]
        file_name=picture.filename
        picture.save(file_name)
        
        im = image.load_img(file_name, target_size=(28,28), color_mode="grayscale")
        pixel_array = img_to_array(im)

        # this block changes the white background to a black background
        # which is needed for accurate predictions
        for row in pixel_array:
            for pixel in row:
                if pixel[0]>=235:
                    pixel[0]=0
        
        pixel_array /= 255

        # the model expects an array of several images so we add an extra
        # dimension to our one image
        pixel_array = np.expand_dims(pixel_array, axis = 0)
        
        # the model spits out a list of answers so we need to grab the 
        # first and only answer it gives
        # answer=model.predict_classes(pixel_array)[0]
        # answer=class_names[answer]
        predictions = model.predict(pixel_array)
        answer=class_names[np.argmax(predictions)]

        return render_template("imageUpload.html",picture=f"input/{file_name}",message=answer)
        

    return render_template("imageUpload.html")

@app.route("/input/<file>")
def input(file):
    return send_from_directory("",f"{file}")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

# @app.route("/generic")
# def generic():
#     return render_template("generic.html")

@app.route("/model")
def model():
    return render_template("model.html")

# @app.route("/elements")
# def elements():
#     return render_template("elements.html")

@app.route("/visual")
def visual():
    return render_template("visual.html")

if __name__ == "__main__":
    app.run(debug=True)