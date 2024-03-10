# -*- coding: utf-8 -*-
from flask import Flask, render_template,request
import json
import base64
from data_config import Config_data
from matplotgraphics import MatGrapics
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] ='secret_key_012347'

@app.route('/')
def index():
    ins = MatGrapics()
    data = ins.get_json_data()
    return render_template('index.html', health_data=data)
    
@app.route('/regist_data', methods=['GET','POST'])
def regist_data():
    if request.method =='POST':
        high = request.form.get('high_bld')
        low = request.form.get('low_bld')
        pulse = request.form.get('pulse')
        weight = request.form.get('weight')
        return render_template('confirm.html', high=high, low=low,
            pulse=pulse,weight=weight)

@app.post('/confirm')
def confirm_data():
    # get data
    data = {
        "dt": datetime.date.today().strftime("%Y-%m-%d"),
        "high": int(request.form.get('high_bld')),
        "low": int(request.form.get('low_bld')),
        "pulse": int(request.form.get('pulse')),
        "weight": float(request.form.get('weight'))
    }
    ins = Config_data(data)
    ins.add_new_data()

    userInput = request.form.get('userInput')
    
    if userInput == "True":
        # print('registed this name')
        return render_template('thanks.html')
    else:
        # print('cancel this regist name')
        high = request.form.get('high_bld')
        low = request.form.get('low_bld')
        pulse = request.form.get('pulse')
        weight = request.form.get('weight')
        return render_template('confirm.html', high=high, low=low,
            pulse=pulse,weight=weight)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8000', debug=True)