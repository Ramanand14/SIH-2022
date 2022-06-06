from flask import Flask, render_template, Response, request
import cv2
import numpy as np
import os, sys
import datetime, time
from threading import Thread

from flask import Flask,render_template,Response
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from keras.preprocessing.image import img_to_array
import os
import tensorflow as tf

model = load_model(r'keras_model.h5')


global capture,rec_frame,  switch,  rec, out 
capture=0
switch=0
rec=0

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:
            try:
                #flip the camera feed horizontally
                frame = cv2.flip(frame, 1)
                ret, buffer = cv2.imencode('.jpg', frame)
            
            #start prediction code:
                img_array = cv2.resize(buffer, (224, 224))
                img_array = np.array(img_array)
                img_array = np.stack((img_array,)*3, axis = -1)
                img_array = np.expand_dims(img_array, axis = 0)
                list = ["Male", "Female", "No Human"]
                prediction = model.predict(img_array)
                x = np.argmax(prediction)
            #text = list[x]
                print(list[x])
            #end of prediction
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

#instatiate flask app  
app = Flask(__name__, template_folder='template/HTML')
#camera = cv2.VideoCapture(0)
@app.route('/')
def index():
    return render_template('camera.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        
        if  request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
                
            else:
                camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                switch=1
        
                          
                 
    elif request.method=='GET':
        return render_template('camera.html')
    return render_template('camera.html')
#camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
if __name__ == '__main__':
    app.run()
    
