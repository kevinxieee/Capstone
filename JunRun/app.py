from flask import Flask, render_template, Blueprint
#import Chart from 'chart.js'
app = Flask(__name__)

#@app.route("/home")
@app.route('/')

def home():
    return render_template("index.html")


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8000, debug=True)
    app.run()