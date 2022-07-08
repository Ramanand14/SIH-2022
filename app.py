from urllib import request
from flask import Flask, request, render_template, Response

import cv2
import cvzone
import mysql.connector
import numpy as np

from mysql.connector import Error
from cvzone.HandTrackingModule import HandDetector

app = Flask(__name__, template_folder='template/HTML')

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "", database="user_details")

switch1, i = 0, 0

camera = cv2.VideoCapture(0)
camera.release()
cv2.destroyAllWindows()  

detector = HandDetector(detectionCon=0.5, maxHands=1)

def gen_frames():
    while True:
        global i
        success, frame = camera.read() 

        #flip the camera feed horizontally
        frame = cv2.flip(frame, 1)

        font = cv2.FONT_HERSHEY_SIMPLEX
  
        # putText() method for inserting text on video
        cv2.putText(frame, 'TEXT ON VIDEO', (5, 30), font, 1, (0, 255, 255), 1, cv2.LINE_4)
        
        #detect the hand in the frame
        hands, img = detector.findHands(frame)
        
        ret, buffer = cv2.imencode('.jpg', frame)

        #find the landmarks of the hand
        a = "bbox"
        b = [hands_dict[a] for hands_dict in hands]
        b = np.array(b)

        if len(b) != 0:
            #get the boundary points of hand area
            cropped_img = img[b[0][1] : b[0][1] + b[0][3], b[0][0] : b[0][0] + b[0][2]]
            #save separetly the only hand image
            image = cv2.imencode('.jpg', cropped_img)

            cv2.imwrite('img'+str(i)+'.jpeg',cropped_img)
            i += 1
            #remove the color from the hand and convert to gray image
            im = cv2.cvtColor(cropped_img, cv2.COLOR_RGB2GRAY)
        
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

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch1, camera
    if request.method == 'POST':
        if  request.form.get('stop') == 'Stop/Start':
            if(switch1==1):
                switch1=0
                camera.release()
                cv2.destroyAllWindows()  
            else:
                camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                switch1=1      
    elif request.method=='GET':
        return render_template('home.html')
    
    return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True)