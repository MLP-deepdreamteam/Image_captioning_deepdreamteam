# app.py
from flask import Flask, render_template, request, jsonify
import os
import tensorflow as tf 
import keras
from keras.utils import load_img, img_to_array 
import numpy as np
from PIL import Image
import requests
import json
from datetime import datetime
import sqlite3
import base64
from io import BytesIO




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


# naver papago open api 
# def translate(text, source='en', target='ko'):
#     CLIENT_ID, CLIENT_SECRET = 'iICkLuA8cumOEp9WwpWR', 'qJyQVZ7yNj'
#     url = 'https://openapi.naver.com/v1/papago/n2mt'
#     headers = {
#         'Content-Type': 'application/json',
#         'X-Naver-Client-Id': CLIENT_ID,
#         'X-Naver-Client-Secret': CLIENT_SECRET
#     }
#     data = {'source': 'en', 'target': 'ko', 'text': text}
#     response = requests.post(url, json.dumps(data), headers=headers)
#     return response.json()['message']['result']['translatedText']
  
  
@app.route('/service',methods=('GET', 'POST')) #url
def index():
    return render_template('index.html')

@app.route('/')  
def home():
    return render_template('home.html')

@app.route('/project')  
def project():
    return render_template('project.html')

@app.route('/predict', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
       
        file = request.files['image']

        filename = file.filename
        filename, extension = os.path.splitext(file.filename)
        new_filename = filename + '.jpg'
        # if filename.split('.mp3') : # 파일명과 확장자분리 만일에 확장자가 .mp3이면 
        #   speak(filename)
          
        # else :
        # file.save(os.path.join('static', filename))
        file_path = os.path.join('static/images',new_filename)
        file.save(file_path)
        images = read_img(file_path)
       
        

        current_time = datetime.now()
        timestamp = int(current_time.timestamp())
        
        id_key = '90'+str(timestamp)
        id_key = int(id_key)
        
         # insert the image data into SQLite
         #DB 연동 테스트
        # conn = sqlite3.connect('coco30k_F_v4.db')
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO customer_image VALUES (?, ?, ?)", (id_key, bi_img, timestamp))
        # conn.commit()
        # conn.close()

        prediction = model.predict(images , batch_size=10)
        if prediction[0] > 0 :
            pred = "This image is a puppy image."
        else :
            pred = 'This image is a cat image.'
        # trans = translate(pred)
        
        
    return render_template('predict.html', fileimg = file_path , pred = pred, id_key = id_key)
    
# def speak(text):

#      tts = gTTS(text=text, lang='en')

#     #  filename='hi.mp3'
    
#      tts.save(filename)

#      playsound.playsound(filename)



# speak('안녕핫요ㅕ')

if __name__=="__main__":
  app.run(debug=True)
  # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)