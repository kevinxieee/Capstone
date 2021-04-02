########  imports  ##########
from flask import Flask, jsonify, request, render_template
import json
import pandas as pd
import weather_scraper, Optimization_Baseline, Optimization_Function_wEA, Optimization_Function_wRevenue


app = Flask(__name__)

# data = list(range(1,300,3))
# print (data)

@app.route('/')
def home_page():
    return render_template('index.html')



######## Data fetch ############
@app.route('/getdata', methods=['GET','POST'])
def data_get():
    
    if request.method == 'POST': # POST request
        print(request.get_text())  # parse as text
        return 'OK', 200
    
    else: # GET request
        a = Optimization_Baseline.getData()
        b = Optimization_Function_wEA.getData()
        c = Optimization_Function_wRevenue.getData()
        
        json_data = json.dumps({**a, **b, **c})

        return jsonify(json_data)


app.run(debug=True)