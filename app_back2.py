from asyncio.windows_events import NULL
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

app = Flask(__name__, template_folder='template/HTML')
camera = cv2.VideoCapture(0)
#text = ""

def generate_frames():
    #global text
    while True:
        # read the camera frame
        success,frame = camera.read()
        if not success:
            break
        else:
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
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    #global text
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)