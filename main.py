# -*- coding: utf-8 -*-
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, send_file, render_template,request,flash
import json
import base64
from data_config import Config_data
from matplotgraphics import MatGrapics
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] ='secret_key_012347'

def create_graph():
    
    image = io.BytesIO()
    ins = MatGrapics()
    fig = ins.create_blood()
    fig.savefig(image, format='png')
    image.seek(0)
    return base64.b64encode(image.getvalue()).decode('utf-8')

@app.route('/')
def index():
    # グラフを作成
    image_base64 = create_graph()
    return render_template('index.html', image_data=image_base64)
    
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
        "high": int(request.form.get('high')),
        "low": int(request.form.get('low')),
        "pulse": int(request.form.get('pulse')),
        "weight": float(request.form.get('weight'))
    }
    ins = Config_data(data)
    ins.add_new_data()

    userInput = request.form.get('userInput')
    
    if userInput == "True":
        print('registed this name')
    else:
        print('cancel this regist name')
    return render_template('thanks.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8000', debug=True)