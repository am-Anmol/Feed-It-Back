from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app=Flask(__name__,static_url_path='/static')
app.secret_key = "4db8ghfhb51a4017e427f3ea5c2137c450f767dce1bf"  

app.config['MYSQL_HOST'] = 'localhost'#hostname
app.config['MYSQL_USER'] = 'root'#username
app.config['MYSQL_PASSWORD'] = '1234'#password G@nesh24

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
        flash('Account exists')
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

@app.route("/volunteerRegister", methods = ["POST"])
def volunteer_reg():
    
    fullname = request.form['full_name']
    phoneno = request.form['phoneno']
    location = request.form['location']
    email = request.form['email']
    password = request.form['password']
    cnf_password = request.form['confirm_password']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM volunteer WHERE email = % s', (email, ))
    account = cursor.fetchone()
    

    if account:
        flash('Account Exists')
        return redirect(url_for("vregister"))
    elif len(phoneno) != 10:
        flash("Please enter a valid phone number")
        return redirect(url_for("vregister"))
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        flash("Please enter a valid email")
        return redirect(url_for("vregister"))
    elif password != cnf_password:
        flash("Password don't Match")
        return redirect(url_for("vregister"))
    else:
        cursor.execute('INSERT INTO volunteer(v_name, v_location, v_contact_number, email, vl_password) VALUES (%s, %s, %s, %s, %s)', 
                (fullname, location, phoneno, email, password))
        mysql.connection.commit()
        #flash = 'You have successfully registered !'
        return redirect(url_for("login"))

@app.route('/logged', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s AND passwd = % s', (email, password))
        account = cursor.fetchone()
        if account:
            session['email'] = account['email']
            session['type']=account ['userType']
            msg = 'Logged in successfully !'
            if session['type'] == 'donor':
                return redirect('/donorhome')
            elif session['type'] == 'volunteer':
                return redirect('/volunteerhome')
            else:
                return session['email'] +' '+ session['type'] 
            #admin dashboard left

        else:

            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('type', None)
    return redirect(url_for('login'))

@app.route("/login")
def lgn():
    return render_template('login.html')

@app.route("/foodhistory")
def fhistory():
    return render_template('foodhistory.html')


@app.route("/donorhome")
def dhome():
    return render_template('homedo.html')

@app.route("/donordashboard")
def donordashboard():
    return render_template('dashdo.html')

@app.route("/managefooddonor")
def donormanage():
    return render_template('managefooddo.html')

@app.route("/addfood")
def addfood():
    return render_template('addfooddo.html')

@app.route("/volunteerhome")
def vhome():
    return render_template('homevo.html')

@app.route("/volunteerdashboard")
def volunteerdashboard():
    return render_template('dashvo.html')

@app.route("/requestfood")
def requestfood():
    return render_template('RequestFood.html')

app.run(debug=True)
