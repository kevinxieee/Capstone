########  imports  ##########
from flask import Flask, jsonify, request, render_template
import json
import pandas as pd
import weather_scraper, Weather_Module_Baseline, Weather_Module_wEA, Weather_Module_wRevenue
import Optimization_Baseline, Optimization_Function_wEA, Optimization_Function_wRevenue


app = Flask(__name__)

# data = list(range(1,300,3))
# print (data)

@app.route('/')
def home_page():
    return render_template('index.html')

######## Historical Data Optimizer  ############
@app.route('/getdata', methods=['GET','POST'])
def optData():
    
    if request.method == 'POST': # POST request
        print(request.get_text())  # parse as text
        return 'OK', 200
    
    else: # GET request
        a = Optimization_Baseline.getData()
        b = Optimization_Function_wEA.getData()
        c = Optimization_Function_wRevenue.getData()
        
        json_data = json.dumps({**a, **b, **c})

        return jsonify(json_data)

######## Historical Data Optimizer  ############
@app.route('/getweather', methods=['GET','POST'])
def weatherData():
    
    if request.method == 'POST': # POST request
        print(request.get_text())  # parse as text
        return 'OK', 200
    
    else: # GET request
        a = Weather_Module_Baseline.getData()
        b = Weather_Module_wEA.getData()
        c = Weather_Module_wRevenue.getData()
        
        json_data = json.dumps({**a, **b, **c})

        return jsonify(json_data)


app.run(debug=True)