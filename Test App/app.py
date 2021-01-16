from flask import Flask, request, jsonify, render_template, redirect
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)

allowed_files = ["JPEG", "JPG", "PNG", "GIF"]
max_image = 0.5 * 1024 * 1024

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in allowed_files:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= max_image:
        return True
    else:
        return True


@app.route("/", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":
        print("first")

        if request.files:
            print("second")

            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                print(filename)
                image.save(filename)

                print("Image saved")

                return render_template("file_upload_test.html", picture=filename)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    return render_template("file_upload_test.html")

if __name__ == "__main__":
    app.run(debug=True)