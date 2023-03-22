# app.py
from flask import Flask, render_template, request
import os
import tensorflow as tf 
import keras
from keras.utils import load_img, img_to_array 
import numpy as np
from PIL import Image


#Flask 객체 인스턴스 생성
app = Flask(__name__)
model = tf.keras.models.load_model('dog_cat_model.h5')

def read_img(fname) :
  img = load_img(fname , target_size=(150,150))
  x = img_to_array(img) 
  images = np.expand_dims(x, axis=0)
#   images = images.astype('float')
#   images = images / 255.0
  return images

@app.route('/',methods=('GET', 'POST')) # 접속하는 url
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
       
        file = request.files['file']
        filename = file.filename
        # file.save(os.path.join('static', filename))
        file_path = os.path.join('static/images',filename)
        file.save(file_path)
        images = read_img(file_path)
        prediction = model.predict(images , batch_size=10)
        if prediction[0] > 0 :
            pred = "강아지"
        else :
            pred = '고양이'
        
    print(file)
    print(filename)
    print(pred)
    return render_template('predict.html', fileimg = file_path , pred = pred)
    

if __name__=="__main__":
  app.run(debug=True)
  # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)