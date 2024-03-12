# -*- coding: utf-8 -*-
from flask import Flask, render_template,request
import json
import base64
from data_config import Config_data
from matplotgraphics import MatGrapics
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from mysql_tool import DB_Connector

app = Flask(__name__, static_folder='./static')
app.config['SECRET_KEY'] ='secret_key_012347'

@app.route('/')
def index():
    # ins = MatGrapics()
    # data = ins.get_json_data()
    ins = DB_Connector()
    data = ins.sharpe_data_to_graph(1)

    return render_template('index.html', health_data=data)
    
@app.route('/regist_user', methods=['GET','POST'])
def regist_public_user():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        mail_address = request.form.get('email')
        passwd = request.form.get('passwd')
        hash_key = generate_password_hash(password=passwd, salt_length=8)
        return 'success', 200


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

    # ins = Config_data(data)
    # ins.add_new_data()

    userInput = request.form.get('userInput')
    
    if userInput == "True":
        # データ送信(DB登録)
        ins = DB_Connector()
        data_list = [
            datetime.date.today().strftime("%Y-%m-%d"),
            int(request.form.get('high_bld')),
            int(request.form.get('low_bld')),
            int(request.form.get('pulse')),
            float(request.form.get('weight'))
        ]
        ins.insert_health_data(data_list)
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