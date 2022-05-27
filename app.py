from flask import Flask,render_template,request
import mysql.connector
app=Flask(__name__, template_folder = 'template')

mydb=mysql.connector.connect(host="localhost",user="root",passwd="123456")


if mydb.is_connected():
    print("Successfully Connected...")
else:
    print("Some Connectivity Issue Occured....")

#creating the database
# mycursor=mydb.cursor()
# query="create database orchid;"
# mycursor.execute(query)

# mycursor=mydb.cursor()
# mycursor.execute("use xyz")
# query = "create table User1(roll int , name varchar(20))"
# mycursor.execute(query)

@app.route('/')
def index():
    return render_template("sign_up.html")

@app.route('/login', methods=['POST','GET'])
def p():
    if request.method=='POST':
        user=request.form['Email']
        age=request.form['Age']
        password=request.form['Password']
        cpass=request.form['cpass']
        mycursor=mydb.cursor()
        mycursor.execute("use  abc")
        sql = "insert into user4(email,Age,password) values(%s, %s,%s)"
        val = (user,age,password)
        mycursor.execute(sql, val)
        mydb.commit()
        mydb.rollback()
        print("Data Inserted Successfully......")
        mydb.close()
            
        if password==cpass:
            print(user)
            print(age)
            print(password)
            print(cpass)
            return render_template('get.html', uname=user,a=age,pas=password,cpassword=cpass)

if __name__=="main_":
    app.run(debug=True)