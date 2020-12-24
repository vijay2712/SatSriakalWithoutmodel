from flask import Flask , render_template , request, redirect
from datetime import datetime
from model_files import NRI_NDVI, RGB_VARI, stiching
import cv2 , os
# import matplotlib.pyplot as plt
# from keras.models import model_from_json
# import numpy as np
# from keras.preprocessing import image
from glob import glob

app = Flask(__name__)
app.config["NRI_UPLOADS"] = "NRI_image/"
app.config["RGB_UPLOADS"] = "RGB_image/"
# app.config['PLANT_UPLOAD'] = "Plant_image/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@app.route('/', methods=['POST' , 'GET'])
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/NRI_NDVI', methods=['POST' , 'GET'])
def nir_ndvi():
    if request.method == 'POST':
        image = request.files["nriImage"]
        if image and allowed_file(image.filename):
            image.save(os.path.join(app.config["NRI_UPLOADS"], image.filename))
            img = read_image('NRI_image' , image.filename )
            output_image = NRI_NDVI.Ndvi(img , image.filename)
            try:
                return render_template('/NRI_NDVI.html' , image_name = output_image)
            except Exception as e:
                print(e)
                return 'There was an error adding your image {}'.format(e)
    else:
        return render_template('/NRI_NDVI.html')


@app.route('/Rgb_Vari', methods=['POST' , 'GET'])
def rgb_vari():
    if request.method == 'POST':
        image = request.files["rgbImage"]
        if image and allowed_file(image.filename):
            image.save(os.path.join(app.config["RGB_UPLOADS"], image.filename))
            img = read_image('RGB_image' ,image.filename )
            output_image = RGB_VARI.RGB(img , image.filename)
            print(output_image)
            try:
                return render_template('/Rgb_Vari.html' , image_name = output_image)
            except Exception as e:
                print(e)
                return 'There was an error adding your image {}'.format(e)
    else:
        return render_template('/Rgb_Vari.html')


def read_image(folder , image):
    img = cv2.imread('{}\{}'.format(folder,image))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


@app.route('/stitching', methods=['GET', 'POST'])
def image_stitch():
    if request.method == 'POST':
        folder_name = request.form['folder_name']
        folder_ =  'Images_to_stitch/'+folder_name+'/'
        if not os.path.exists(folder_):
            os.makedirs(folder_)

        uploaded_files = request.files.getlist("images")
        for image in uploaded_files:
            if image and allowed_file(image.filename):
                image.save(os.path.join(folder_, image.filename))
        cv_img = []
        for img in glob('{}*.jpg'.format(folder_)):
            img = cv2.imread(img, cv2.IMREAD_COLOR)
            cv_img.append(img)
        output=stiching.Stich(cv_img , folder_name)
        print(output)
        if output.find('.jpg') == -1:
            error = output
            return render_template('Stitch.html',error = error)
        else:
            output_image = output
            return render_template('Stitch.html',output_image = output_image)
    return render_template('Stitch.html')


if __name__=="__main__":
    app.run(debug = True)