import os
from flask import Flask,render_template,request,jsonify,redirect
#from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker,Session

Database_url="postgres://fohlyfbheobcwn:9aac05c70e29aedf00762800caa0f8b7d173528403b8aa4ce5bece859d878d64@ec2-174-129-255-26.compute-1.amazonaws.com:5432/dbjj03i1i59rte"

app = Flask(__name__)

app.config["SESSION_PERMENANT"]=False
app.config["SESSION_TYPE"]="filesystem"
app.static_folder='static'
app.template_folder='templates'
prt=os.getenv('port')

engine=create_engine(Database_url)
db=scoped_session(sessionmaker(engine))

@app.route("/")
def index():
    lstate=request.args.get("lstate")
    return render_template("home.html",lstate=lstate)

@app.route("/login")
def login():
    course=request.args.get("course")
    lstate=request.args.get("lstate")
    if lstate == 'True':
        return content(course)
    return render_template("index.html",lgstat=True,course=course)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/ssign",methods=["POST","GET"])
def ssignup():
    if request.method == "GET":
        return render_template("index.html")
    email=request.form.get("email")
    pname=request.form.get("pname")
    sname=request.form.get("sname")
    scname=request.form.get("scname")
    password=request.form.get("password")
    cno=request.form.get("contactno")

    try:
        db.execute("insert into signup values(default,:email,:pname,:sname,:scname,:pass,:lstate)"
        ,{"email":email,"pname":pname,"sname":sname,"scname":scname,"pass":password,"lstate":'False'})
        db.commit()
    except:
        pass
    return render_template("index.html",jst_signuped=True)

@app.route("/llogin",methods=["POST","GET"])
def llogin():
    if request.method=='GET':
        return render_template("index.html",lstate='False')
    course=request.args.get("course")
    email=request.form.get("email")
    password=request.form.get("password")
    # lstate='False'
    try:
        temp=list(db.execute("select lstate from signup where email=:email limit 1",{'email':email}))
        lstate=temp[0][0]
    except:
        pass

    db.execute("update signup set lstate='True' where email=:email",{'email':email})
    db.commit()
        
    raw_cpass=list(db.execute("select pass from signup where email=:email",{"email":email}))
        
    try:
        cpass=raw_cpass[0][0]
    except IndexError:
        return render_template("index.html",lgstat=False)

    print(f"\n\n>> entered pass = {password} \t correct pass = {cpass} \n\n")
    # print(f"\n\n>> type(entered pass) = {(password)} \t type(correct pass) = {(cpass[0:len(password)])} \n\n")
    print(len(password)==len(cpass))

    if password == cpass[:len(password)]:
    # return render_template("home.html")
        print("congrats you are logged in !")
        # return ("congrats you are logged in !")
        return content(course)
        # return (f"entered pass = {password} correct pass = {cpass}")  
    # return ("congrats you are logged in !")
    # return render_template("content.html",course=course)
    return render_template('home.html',lstate="False")

@app.route("/logout")
def logout():
    # db.execute("update signup set lstate='False' where email=:email",{'email':email})
    # db.commit()
    return render_template("home.html",lstate='False')

def content(course):
    #  email=request.args.get("email")
    # try:
    #     temp=list(db.execute("select lstate from signup where email=:email",{'email':email}))
    #     lstate=temp[0][0]
    # course=request.args.get("course")
    print(f"\n\ncourse = {course} ")
    # if course == None:
        # return render_template("home.html")
        # course="tbrush"
    return render_template("content.html",course=course)

@app.route("/tc")
def tc():
    course=request.args.get("course")
    return render_template("content.html",course=course)

@app.route("/test")
def test():
    course=request.args.get("course")
    return render_template("test.html",course=course)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0', port=port)