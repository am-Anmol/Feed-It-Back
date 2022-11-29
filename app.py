from flask import *
app=Flask(__name__,static_url_path='/static')


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

app.run(debug=True)
