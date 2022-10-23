from cProfile import label
from msilib import CreateRecord
from urllib import request
from flask import Flask, request, render_template, Response

import cv2
import cvzone
import mysql.connector
import numpy as np
import keyboard
import math

from mysql.connector import Error
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

classifier = Classifier("keras_model.h5", "labels.txt")

app = Flask(__name__, template_folder='template/HTML')

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "", database="user_details")

result=' '
switch1, len, imgSize = 0, 20, 300
labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

camera = cv2.VideoCapture(0)
camera.release()
cv2.destroyAllWindows()  

detector = HandDetector(detectionCon=0.5, maxHands=1)

def gen_frames():
    global result
    while True:
        success, frame = camera.read() 

        #flip the camera feed horizontally
        frame = cv2.flip(frame, 1)
  
        imgOut = frame.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        #detect the hand in the frame
        hands, img = detector.findHands(frame)
        
        #find the landmarks of the hand
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255
            cropped_img = img[y-len:y+h+len, x-len:x+w+len]

            aspectRatio = h/w

            if aspectRatio > 1:
                k = imgSize/h
                wCal = math.ceil(k*w)
                imgResize = cv2.resize(cropped_img, (wCal, imgSize))
                wGap = math.ceil((imgSize-wCal)/2)
                imgWhite[:, wGap:wCal+wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
            
            else:
                k = imgSize/w
                hCal = math.ceil(k*h)
                imgResize = cv2.resize(cropped_img, (imgSize, hCal))
                hGap = math.ceil((imgSize-hCal)/2)
                imgWhite[hGap:hCal+hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
            
            #cv2.imshow('Hand', imgWhite)
            if keyboard.is_pressed("enter"):
                result = result + labels[index]
            
            # putText() method for inserting text on hand boundaries
            cv2.putText(imgOut, labels[index], (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 1, cv2.LINE_4)
            
            #draw border around detected hand
            cv2.rectangle(imgOut, (x - len, y - len), (x+w+len, y+h+len), (0, 0, 0), 4)

            #remove the color from the hand and convert to gray image
            #im = cv2.cvtColor(imgWhite, cv2.COLOR_RGB2GRAY)
        
        # putText() method for inserting text on video
        cv2.putText(imgOut, 'Text:' + result, (5, 30), font, 1, (0, 255, 255), 1, cv2.LINE_4)
        cv2.waitKey(1)
        ret, buffer = cv2.imencode('.jpg', imgOut)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_up', methods=['POST','GET'])
def sign_up():
    try:
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            age = request.form['age']
            password = request.form['password']
            rpassword = request.form['rpassword']
            mycursor = mydb.cursor()
            mycursor.execute("insert into user_credentials (username, email, age, password) values(%s, %s, %s, %s)", (username, email, age, password))
            mydb.commit()
            mycursor.close()
    except Error as e:
        print(e)
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        mycursor = mydb.cursor()
        mycursor.execute("select * from user_credentials where email = '" + email + "'and password = '" + password + "'")
        r = mycursor.fetchall()
        count = mycursor.rowcount
        if count == 1:
            return render_template('home.html')
        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/learning', methods=['POST', 'GET'])
def learning():
    return render_template('learning.html')

@app.route('/virtual', methods=['POST', 'GET'])
def virtual():
    return render_template('virtual.html')

@app.route('/keybored', methods=['POST', 'GET'])
def keybored():
    return render_template('keybored.html')

@app.route('/quizmain', methods=['POST', 'GET'])
def quizmain():
    return render_template('quizmain.html')

@app.route('/section1', methods=['POST', 'GET'])
def section1():
    return render_template('section1.html')

@app.route('/section2', methods=['POST', 'GET'])
def section2():
    return render_template('section2.html')

@app.route('/section3', methods=['POST', 'GET'])
def section3():
    return render_template('section3.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch1, camera, result
    if request.method == 'POST':
        if  request.form.get('stop') == 'Stop/Start':
            if(switch1==1):
                result = ' '
                switch1=0
                camera.release()
                cv2.destroyAllWindows()  
            else:
                result = ' '
                camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                switch1=1      
    elif request.method=='GET':
        return render_template('home.html')
    
    return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True)


#44.00 min - Testing Code