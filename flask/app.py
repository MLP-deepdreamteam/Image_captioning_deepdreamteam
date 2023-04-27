# app.py
from flask import Flask, render_template, request, jsonify
import os
import tensorflow as tf 
import keras
from tensorflow.keras.utils import load_img, img_to_array 
import numpy as np
from PIL import Image
import requests
import json
from datetime import datetime
import sqlite3
import base64
from io import BytesIO

import our_model
import feature_extract
import test_tts



#Flask 객체 인스턴스 생성
app = Flask(__name__)
# model = tf.keras.models.load_model('dog_cat_model.h5')
flag=0
print(flag)
def read_img(fname) :
  img = load_img(fname , target_size=(150,150))
  x = img_to_array(img) 
  images = np.expand_dims(x, axis=0)
  images = images.astype('float')
  images = images / 255.0
  return images


# naver papago open api 
def translate(text, source='en', target='ko'):
    CLIENT_ID, CLIENT_SECRET = 'iICkLuA8cumOEp9WwpWR', 'qJyQVZ7yNj'
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    headers = {
        'Content-Type': 'application/json',
        'X-Naver-Client-Id': CLIENT_ID,
        'X-Naver-Client-Secret': CLIENT_SECRET
    }
    data = {'source': 'en', 'target': 'ko', 'text': text}
    response = requests.post(url, json.dumps(data), headers=headers)
    
    print("translation on Process")
    return response.json()['message']['result']['translatedText']

  
@app.route('/service',methods=('GET', 'POST')) #url
def index():
    # if request.method == 'POST':
       
    #     file = request.files['image']
        
    #     # img = Image.open(file)
    #     # img = img.resize((420, 420))

    #     filename = file.filename
    #     filename, extension = os.path.splitext(file.filename)
    #     new_filename = filename + '.jpg'
    #     # if filename.split('.mp3') : # 파일명과 확장자분리 만일에 확장자가 .mp3이면 
    #     #   speak(filename)
          
    #     # else :
    #     # file.save(os.path.join('static', filename))
    #     file_path = os.path.join('static/images',new_filename)
    #     file.save(file_path)
    #     convert_to_jpeg(file_path,file_path)

    #     # images = read_img(file_path)
       
        

    #     current_time = datetime.now()
    #     timestamp = int(current_time.timestamp())
        
    #     id_key = '90'+str(timestamp)
    #     id_key = int(id_key)
        
    #      # insert the image data into SQLite
    #      #DB 연동 테스트
    #     # conn = sqlite3.connect('coco30k_F_v4.db')
    #     # cursor = conn.cursor()
    #     # cursor.execute("INSERT INTO customer_image VALUES (?, ?, ?)", (id_key, bi_img, timestamp))
    #     # conn.commit()
    #     # conn.close()
        
    #     caption_model = our_model.define_our_model()
    #     our_model.load_model(caption_model)
    #     pred = feature_extract.extract_caption(file_path,caption_model)

    #     # prediction = model.predict(images , batch_size=10)
    #     # if prediction[0] > 0 :
    #     #     pred = "This image is a puppy image."
    #     # else :
    #     #     pred = 'This image is a cat image.'
    #     # trans = translate(pred[7:-5])
    #     trans = '테스트용입니다.'
    #     test_tts.create_tts(trans)
    #     audio_file = 'static/audios/output.mp3'
        
        
    #     return render_template('index.html', fileimg = file_path , pred = pred[7:-5], id_key = id_key, trans = trans, audio_file = audio_file)
    return render_template('index.html')

@app.route('/')  
def home():
    return render_template('home.html')

@app.route('/project')  
def project():
    return render_template('project.html')

@app.route('/predict', methods=['GET','POST'])
def upload():
       
    global caption_model, CNN_Encoder, flag 

    if flag ==0: 
        caption_model = our_model.define_our_model()
        our_model.load_model(caption_model)
        CNN_Encoder = feature_extract.define_CNN_Encoder()
        flag +=1 

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
        # features

        
        # feature = feature_extract.extract_features(file_path, CNN_Encoder)
        # print(type(feature), feature.shape)
        pred = feature_extract.extract_caption(file_path,caption_model,CNN_Encoder)

        # trans = "대기"
        trans = translate(pred[7:-5])
        test_tts.create_tts_to_en(pred[7:-5])
        test_tts.create_tts_to_ko(trans)
        audio_file_en = 'static/audios/output_en.mp3'
        audio_file_ko = 'static/audios/output_ko.mp3'
        
        
    return render_template('predict.html', fileimg = file_path , pred = pred[7:-5], id_key = id_key, trans = trans , audio_file_en = audio_file_en , audio_file_ko = audio_file_ko)
@app.route('/about')  
def about():
    return render_template('about.html')    
# def speak(text):

#      tts = gTTS(text=text, lang='en')

#     #  filename='hi.mp3'
    
#      tts.save(filename)

#      playsound.playsound(filename) 
# def speak(text):

#      tts = gTTS(text=text, lang='en')

#     #  filename='hi.mp3'
    
#      tts.save(filename)

#      playsound.playsound(filename)



# speak('안녕핫요ㅕ')

if __name__=="__main__":
  #app.run(debug=True)
  # host 등을 직접 지정하고 싶다면
  app.run(host="0.0.0.0", port="9000", debug=True)
