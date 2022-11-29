from flask import *
app=Flask(__name__,static_url_path='/static')


@app.route("/")
def Index():
    return render_template('index.html')

@app.route("/aboutus")
def about():
    return render_template('aboutus.html')

app.run(debug=True)
