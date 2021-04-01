########  imports  ##########
from flask import Flask, jsonify, request, render_template
import pandas as pd
import weather_scraper


app = Flask(__name__)

# data = list(range(1,300,3))
# print (data)

@app.route('/')
def home_page():
    example_embed='This string is from python'
    return render_template('index.html', embed=example_embed)

@app.route('/test', methods=['GET', 'POST'])
def testfn():
    # GET request
    if request.method == 'GET':
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Success', 200

######## Data fetch ############
@app.route('/getdata', methods=['GET','POST'])
def data_get():
    
    if request.method == 'POST': # POST request
        print(request.get_text())  # parse as text
        return 'OK', 200
    
    else: # GET request
        weather_scraper.getData(); 
        df = pd.read_csv('weather_data.csv');
        print(df)
        data = df.to_json(orient= "split")
        return jsonify(data)
        # return 't_in = %s ; result: %s ;'%(index_no, data[int(index_no)])

app.run(debug=True)