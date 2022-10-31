from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
app = Flask(__name__)
app.secret_key='a'
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mpf67194;PWD=iCG3PvOYvDiHMrq8",'','')
@app.route('/')
def index():
   return render_template('index.html')
@app.route('/login', methods =['GET', 'POST'])
def login(): 
    global userid
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
       email = request.form['email']
       password = request.form['password']
       stmt = ibm_db.prepare(conn,'SELECT * FROM donors WHERE email = ? AND password = ?')
       ibm_db.bind_param(stmt,1,email)
       ibm_db.bind_param(stmt,2,password) 
       ibm_db.execute(stmt)
       account = ibm_db.fetch_assoc(stmt)
       if account:
         session['loggedin'] = True
         session['email'] = account['EMAIL']
         msg = 'Logged in successfully !'
         return render_template('index.html', msg = msg)
       else:
           msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
@app.route('/logout') 
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None) 
   return redirect(url_for('login'))
@app.route('/register', methods =['GET', 'POST'])
def register(): 
    msg = ''
    if request.method == 'POST':
       name = request.form['name']
       bloodgroup = request.form['blood']
       email = request.form['email']
       phonenumber = request.form['phone']
       password = request.form['password']
       address = request.form['address']
       gender = request.form['gender']
       age = request.form['age']
       district = request.form['district']
       state = request.form['state']
       illness = request.form['illness']
       sql= "SELECT * FROM donors WHERE name = ?"
       stmt = ibm_db.prepare(conn,sql)
       ibm_db.bind_param(stmt,1,name) 
       ibm_db.execute(stmt)
       account = ibm_db.fetch_assoc(stmt)
       if account:
         msg = 'Account already exists !' 
       elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
         msg = 'Invalid email address !' 
       elif not re.match(r'[A-Za-z0-9]+', name):
         msg = 'name must contain only characters and numbers !'
       elif not name or not password or not email:
         msg = 'Please fill out the form !'
       else:
           insert_sql = "INSERT INTO donors VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
           stmt = ibm_db.prepare(conn,insert_sql)
           ibm_db.bind_param(stmt, 1, name)
           ibm_db.bind_param(stmt, 2, bloodgroup) 
           ibm_db.bind_param(stmt, 3, email) 
           ibm_db.bind_param(stmt, 4, phonenumber)
           ibm_db.bind_param(stmt, 5, password)
           ibm_db.bind_param(stmt, 6, address)
           ibm_db.bind_param(stmt, 7, gender)
           ibm_db.bind_param(stmt, 8, age)
           ibm_db.bind_param(stmt, 9, district)
           ibm_db.bind_param(stmt, 10, state)
           ibm_db.bind_param(stmt, 11, illness)
           ibm_db.execute(stmt)
           msg = 'You have successfully registered !'
    return render_template('register.html', msg = msg)
if __name__ == '__main__':
  app.run(debug= True)
