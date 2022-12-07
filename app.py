from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import *

app=Flask(__name__,static_url_path='/static')
app.secret_key = "4db8ghfhb51a4017e427f3ea5c2137c450f767dce1bf"  

app.config['MYSQL_HOST'] = 'localhost'#hostname
app.config['MYSQL_USER'] = 'root'#username

app.config['MYSQL_PASSWORD'] = 'Raghu@2000'#password G@nesh24


app.config['MYSQL_DB'] = 'fib'#database name

mysql = MySQL(app)



@app.route("/")
def Index():
    return render_template('index.html')

@app.route("/aboutus1")
def about():
    return render_template('aboutus1.html')

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
    cursor.execute('SELECT * FROM volunteer WHERE email = % s', (email, ))
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
    cursor.execute('SELECT * FROM donor WHERE email = % s', (email, ))
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
        data = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s AND passwd = % s', (email, password))
        account = cursor.fetchone()
        if account:
            session['email'] = account['email']
            session['type']=account ['userType']
            msg = 'Logged in successfully !'
            if session['type'] == 'donor':
                data.execute('select * from donor where email=%s',(email,))
                details = data.fetchone()
                session['id']=details['donor_id']
                return redirect('/donordashboard')
            elif session['type'] == 'volunteer':
                data.execute('select * from volunteer where email=%s',(email,))
                details = data.fetchone()
                session['id']=details['volunteer_id']
                return redirect('/volunteerdashboard')
            elif session['type'] == 'admin':
                data.execute('select * from admins where email=%s',(email,))
                details = data.fetchone()
                session['id']=details['admin_id']
                return redirect('/dashadmin')
            else:
                return 'You do not belong to our page'

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

def check_type(type):
    ck_type = session.get("type")
    print(ck_type == type)
    if ck_type != None and ck_type == type:
        return True
    else:
        return False

@app.route("/foodhistory")
def fhistory():
    if not check_type("admin"):
        return redirect(url_for("login"))
    return render_template('foodhistory.html')


@app.route("/donorhome")
def dhome():
    if not check_type("donor"):
        return redirect(url_for("login"))
    return render_template('homedo.html')

@app.route("/donordashboard", methods=['GET','POST'])
def donordashboard():
    if not check_type("donor"):
        return redirect(url_for("login"))
    cur=mysql.connection.cursor()
    cur.execute('select count(*) from volunteer')
    no_volunteers=cur.fetchall()
    cur.close()
    return render_template('dashdo.html',no_volunteers=no_volunteers)

@app.route("/managefooddonor", methods=['GET','POST'])
def donormanage():
    if not check_type("donor"):
        return redirect(url_for("login"))
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM food_added where d_id = %s',(session.get("id"),))
    fd=cursor.fetchall()
    cursor.execute('SELECT name FROM donor where donor_id = %s',(session.get("id"),))
    dname=cursor.fetchall()
    cursor.close()
    return render_template('managefooddo.html', fd=fd,dname=dname)

@app.route("/addfood", methods=['GET', 'POST'])
def addfood():
    if not check_type("donor"):
        return redirect(url_for("login"))
    if request.method == 'POST':
        f_qty = request.form['foodqty']
        category = request.form['category']  
        location = request.form['pickuploc']
        duration = request.form['duration']
        status = request.form['status']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO food_added(food_qty, food_cat, f_status, pickup_location, created_time, duration_time,d_id) VALUES (%s, %s, %s, %s, %s,%s, %s)',(f_qty,category,status,location,datetime.now(),duration,session['id']));
        mysql.connection.commit()
        return redirect('/managefooddonor')
    return render_template('addfooddo.html')

@app.route("/volunteerhome")
def vhome():
    if not check_type("volunteer"):
        return redirect(url_for("login"))
    return render_template('homevo.html')

@app.route("/volunteerdashboard", methods=['GET','POST'])
def volunteerdashboard():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT count(*) FROM volunteer')
    no_vol=cursor.fetchall()
    if not check_type("volunteer"):
        return redirect(url_for("login"))
    return render_template('dashvo.html', no_vol=no_vol)

@app.route("/requestfood", methods=['GET', 'POST'])
def requestfood():
    if not check_type("volunteer"):
        return redirect(url_for("login"))
    cur=mysql.connection.cursor()
    cur.execute('select * from food_added f left join volunteer_request r on f.foodid=r.foodId order by f.created_time desc')
    food=cur.fetchall()
    return render_template('RequestFood.html',food=food)

@app.route("/adminhome")
def ahome():
    if not check_type("admin"):
        return redirect(url_for("login"))
    return render_template('homeadmin.html')

@app.route("/dashadmin", methods=['GET', 'POST'])
def admindashboard():
    if not check_type("admin"):
        return redirect(url_for("login"))
    cur=mysql.connection.cursor()
    cur.execute('select count(*) from donor')
    no_donors=cur.fetchall()
    cur.execute('select count(*) from volunteer')
    no_volunteers=cur.fetchall()
    cur.close()
    return render_template('dashadmin.html',no_donors=no_donors, no_volunteers=no_volunteers)

@app.route("/view_donors", methods=['GET', 'POST'])
def viewdonors():
    if not check_type("admin"):
        return redirect(url_for("login"))
    cur=mysql.connection.cursor()
    cur.execute('select * from donor')
    search=None
    if request.method == "POST":
        search=request.form['search']
        sq="%"+search+"%"
        cur.execute('select * from donor WHERE name LIKE %s',(sq,))
    all_donors=cur.fetchall()
    cur.close()
    return render_template('view_donors.html',all_donors=all_donors)




@app.route("/edit_donor/<int:id>", methods=["POST", "GET"])
def updatedonor(id):
    d_id = id
    cur = mysql.connection.cursor()
    cur.execute("Select d_location, d_contact_number, email from donor where donor_id = %s", (id,))
    data = cur.fetchone()


    if request.method == "POST":
        donor_location = request.form['d_location']
        donor_contact = request.form['d_contact_number']
        donor_email = request.form['email']
        cur.execute("Update donor set d_location = %s, d_contact_number = %s, email = %s where donor_id = %s", (donor_location,donor_contact, donor_email, id))
        mysql.connection.commit()
        return redirect(url_for("viewdonors"))
    return render_template("edit_donor.html", **locals())

@app.route("/view_volunteers", methods=['GET', 'POST'])
def viewvols():
    if not check_type("admin"):
        return redirect(url_for("login"))
    cur=mysql.connection.cursor()
    cur.execute('select * from volunteer')
    search=None
    if request.method == "POST":
        search=request.form['search']
        sq="%"+search+"%"
        cur.execute('select * from volunteer WHERE v_name LIKE %s',(sq,))
    all_volunteers=cur.fetchall()
    cur.close()
    return render_template('view_volunteers.html',all_volunteers=all_volunteers)

@app.route("/edit_volunteer/<int:id>", methods=["POST", "GET"])
def updatevolunteer(id):
    v_id = id
    cur = mysql.connection.cursor()
    cur.execute("Select v_location, v_contact_number, email from volunteer where volunteer_id = %s", (id,))
    data = cur.fetchone()


    if request.method == "POST":
        volunteer_location = request.form['v_location']
        volunteer_contact = request.form['v_contact_number']
        volunteer_email = request.form['email']
        cur.execute("Update volunteer set v_location = %s, v_contact_number = %s, email = %s where volunteer_id = %s", (volunteer_location,volunteer_contact, volunteer_email, id))
        mysql.connection.commit()
        return redirect(url_for("viewvols"))
    return render_template("edit_volunteer.html", **locals())

@app.route("/view_foodavailable", methods=['GET', 'POST'])
def view_foodavailable():
    if not check_type("admin"):
        return redirect(url_for("login"))
    cur=mysql.connection.cursor()
    cur.execute('select * from food_added')
    food_available=cur.fetchall()
    cur.close()
    return render_template('view_foodavailable.html',food_available=food_available)

@app.route("/view_foodrequested", methods=['GET', 'POST'])
def view_requests():
    if not check_type("admin"):
        return redirect(url_for("login"))
    cur=mysql.connection.cursor()
    cur.execute('select * from volunteer_request')
    food_requests=cur.fetchall()
    cur.close()
    return render_template('view_foodrequested.html',food_requests=food_requests)

@app.route("/add_receiver")
def add_rec():
    if not check_type("admin"):
        return redirect(url_for("login"))
    return render_template('add_receiver.html')


@app.route("/add_receiver", methods = ["POST"])
def add_receiver():
    if not check_type("admin"):
        return redirect(url_for("login"))
    address = request.form['r_address']
    phoneno = request.form['r_contact_number']
    cursor=mysql.connection.cursor()
    if len(phoneno) != 10:
        flash("Please enter a valid phone number")
        return redirect(url_for("add_rec"))
    else:
        cursor.execute('INSERT INTO reciever(r_address, r_contact_number) VALUES (%s, %s)', 
                (address, phoneno))
        mysql.connection.commit()
        #flash = 'Receiver Successfully Added !'
        return redirect(url_for("admindashboard"))

@app.route("/edit_receiver/<int:id>", methods=["POST", "GET"])
def updatereceivers(id):
    if not check_type("admin"):
        return redirect(url_for("login"))
    r_id = id
    cur = mysql.connection.cursor()
    cur.execute("Select r_address, r_contact_number from reciever where reciever_id = %s", (id,))
    data = cur.fetchone()


    if request.method == "POST":
        receiver_addr = request.form['addr']
        receiver_num = request.form['phoneno']
        cur.execute("Update reciever set r_address = %s, r_contact_number = %s where reciever_id = %s", (receiver_addr, receiver_num, id))
        mysql.connection.commit()
        return redirect(url_for("viewreceivers"))
    return render_template("edit_receiver.html", **locals())

@app.route("/delete_receiver/<int:id>", methods=["POST", "GET"])
def deletereceivers(id):
    if not check_type("admin"):
        return redirect(url_for("login"))
    r_id = id
    cur = mysql.connection.cursor()
    cur.execute("Delete from reciever where reciever_id = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for("viewreceivers"))
    


@app.route("/view_receivers", methods=['GET'])
def viewreceivers():
    if not check_type("admin"):
        return redirect(url_for("login"))
    cur=mysql.connection.cursor()
    cur.execute('select * from reciever')
    receiver=cur.fetchall()
    cur.close()
    return render_template('view_receivers.html',receiver=receiver)

@app.route("/addrequest/<int:fid>/<int:did>", methods=["POST", "GET"])
def addrequest(fid,did):
    cur=mysql.connection.cursor()
    cur.execute('select * from reciever')
    receiver=cur.fetchall()
    return render_template("add_request.html",receiver=receiver,fid=fid,did=did)

@app.route("/add_request/<int:fid>/<int:did>", methods=["POST", "GET"])
def add_request(fid,did):
    cur=mysql.connection.cursor()
    if request.method == 'POST':
        recev = request.form['receiver']
        status = request.form['status']
        cur.execute('Insert into volunteer_request(status, foodId, donorId, recieverId, volunteerId) values(%s,%s,%s,%s,%s)',(status,fid,did,recev,session['id']))
        mysql.connection.commit()
        cur.close()
        return redirect('/requestfood')
    

@app.route("/myrequest", methods=["POST", "GET"])
def myrequest():
    cur=mysql.connection.cursor()
    cur.execute('select * from volunteer_request join reciever on recieverId=reciever_id join donor on donorId=donor_id where volunteerId=%s order by requestId desc',(session['id'],))
    req=cur.fetchall()        
    return render_template("myrequest.html",req=req)

@app.route("/statusrequest/<int:id>", methods=["POST", "GET"])
def statusrequest(id):
    return render_template("updateRequestStatus.html",id=id)

@app.route("/updatestatusrequest/<int:id>", methods=["POST", "GET"])
def updatestatusrequest(id):
    if request.method == 'POST':
        cur=mysql.connection.cursor()
        status = request.form['status']
        cur.execute("Update volunteer_request set status = %s where requestId = %s", (status, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/myrequest')

app.run(debug=True)
