from flask import Flask, render_template, Response, request
import cv2
import numpy as np
import os, sys
import datetime, time
from threading import Thread


global capture,rec_frame,  switch,  rec, out 
capture=0
switch=0
rec=0

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:
               
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)
            
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
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
    
