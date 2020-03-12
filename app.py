from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/buddy/<n>')
def bitch(n):
    if n == 'parker' or n == 'Parker':
        return "<h1>" + n + " is a buddy for sure</h1>"
    else:
        return "<h1>Friend you, " + n + ", buddy</h1>"

