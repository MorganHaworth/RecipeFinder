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

@app.route('/results')
def results():
    return render_template("results.html")

@app.route('/conversions')
def conversions():
    return render_template("convert.html")

def convertResults(cFrom, cTo):

    ratio = [[1,4,8,16,128,256,768],
    [1/4,1,2,4,32,64,192],
    [1/8,1/2,1,2,16,32,96],
    [1/16,1/4,1/2,1,8,16,48],
    [1/128,1/32,1/16,1/8,1,2,6],
    [1/256,1/64,1/32,1/16,1/2,1,3],
    [1/768,1/92,1/96,1/48,1/6,1/3,1]]

    nameToNum = {
        "gallon": 0,
        "quart": 1,
        "pint": 2,
        "cup": 3,
        "ounce": 4,
        "tablespoon": 5,
        "teaspoon": 6
    }

    convFrom = cFrom.split()
    number = int(convFrom[0])
    unitFrom = convFrom[1]
    
    result = number * ratio[nameToNum[unitFrom]][nameToNum[cTo]]

    return str(result) + ' ' + cTo + 's'

@app.route('/convert', methods=['GET','POST'])
def convert():
    convertFrom = request.form['convertFrom']
    convertTo = request.form['convertTo']
    result = convertResults(convertFrom, convertTo)
    return render_template("convertResults.html", result=result)

@app.route('/API')
def recipes():
    return render_template("API-key-test.html", key=API_KEY)
