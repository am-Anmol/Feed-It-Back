from flask import *
from flask_mysqldb import MySQL
import re

app=Flask(__name__,static_url_path='/static')
app.secret_key = "4db8ghfhb51a4017e427f3ea5c2137c450f767dce1bf"  

app.config['MYSQL_HOST'] = 'localhost'#hostname
app.config['MYSQL_USER'] = 'root'#username
app.config['MYSQL_PASSWORD'] = 'G@nesh24'#password

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

@app.route("/donorRegister", methods = ["POST"])
def donor_reg():
    
    fullname = request.form['full_name']
    phoneno = request.form['phoneno']
    location = request.form['location']
    email = request.form['email']
    password = request.form['password']
    cnf_password = request.form['confirm_password']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM donor WHERE email = % s', (email, ))
    account = cursor.fetchone()
    

    if account:
        flash('This is a flash message')
        return redirect(url_for("dregister"))
    elif len(phoneno) != 10:
        print("IN")
        flash("Please enter a valid phone number")
        return redirect(url_for("dregister"))
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        flash("Please enter a valid email")
        return redirect(url_for("dregister"))
    elif password != cnf_password:
        flash("Password don't Match")
        return redirect(url_for("dregister"))
    else:
        cursor.execute('INSERT INTO donor(name, d_location, d_contact_number, email, dn_password) VALUES (%s, %s, %s, %s, %s)', 
                (fullname, location, phoneno, email, password))
        mysql.connection.commit()
        #flash = 'You have successfully registered !'
        return redirect(url_for("login"))


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
