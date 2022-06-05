from urllib import request
from flask import Flask, request, render_template

import mysql.connector
from mysql.connector import Error

app = Flask(__name__, template_folder='template/HTML')

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "", database="user_details")

if mydb.is_connected():
    print("Successfully Connected...")
else:
    print("Some Connectivity Issue Occured....")

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
    return render_template('sign_up.html')

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

if __name__=="__main__":
    app.run(debug=True)