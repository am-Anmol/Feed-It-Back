from flask import *
from flask_mysqldb import MySQL
app=Flask(__name__,static_url_path='/static')
app.secret_key = "4db8ghfhb51a4017e427f3ea5c2137c450f767dce1bf"  

app.config['MYSQL_HOST'] = 'localhost'#hostname
app.config['MYSQL_USER'] = 'root'#username
app.config['MYSQL_PASSWORD'] = '1234'#password

app.config['MYSQL_DB'] = 'fib'#database name

mysql = MySQL(app)


@app.route("/")
def Index():
    return render_template('index.html')

@app.route("/aboutus")
def about():
    return render_template('aboutus.html')

@app.route("/donorRegister")
def dregister():
    return render_template('donorRegister.html')

@app.route("/volunteerRegister")
def vregister():
    return render_template('volunteerRegister.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/foodhistory")
def fhistory():
    return render_template('foodhistory.html')

app.run(debug=True)
