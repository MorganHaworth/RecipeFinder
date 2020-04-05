from flask import render_template, request
import requests
import json
from app import app
import os
API_KEY = os.environ.get('API_KEY')
url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

@app.route('/')
@app.route('/welcome')
def home():
    return render_template("welcome.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/cook')
def cook():
    return render_template("cook.html")

@app.route('/results', methods=['GET','POST'])
def results():
    meats = request.form.getlist('meat')
    return render_template("results.html", meats=meats)

@app.route('/API')
def recipes():
    return render_template("API-key-test.html", key=API_KEY)
