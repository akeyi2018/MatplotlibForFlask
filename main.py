# -*- coding: utf-8 -*-
from flask import Flask, render_template,request
import datetime
from werkzeug.security import generate_password_hash
from mysql_tool import DB_Connector
from settings import Message_list

app = Flask(__name__, static_folder='./static')
app.config['SECRET_KEY'] ='secret_key_012347'

@app.route('/')
def index():
    # ins = MatGrapics()
    # data = ins.get_json_data()
    ins = DB_Connector()
    data = ins.sharpe_data_to_graph(1)

    # データ入力フラグ
    flag = ins.check_date(datetime.date.today().strftime("%Y-%m-%d"))

    event_data = ins.get_event_data(1)

    return render_template('index.html', health_data=data, flag=flag, event_data= event_data)
    
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

    # データを取得する
    high = request.form.get('high_bld')
    low = request.form.get('low_bld')
    pulse = request.form.get('pulse')
    weight = request.form.get('weight')
    
    userInput = request.form.get('userInput')
    
    if userInput == "True":
        # データ送信(DB登録)
        ins = DB_Connector()
        data_list = [
            datetime.date.today().strftime("%Y-%m-%d"),
            int(high),
            int(low),
            int(pulse),
            float(weight)
        ]
        ins.insert_health_data(data_list)
        return render_template('thanks.html')
    else:
        return render_template('confirm.html', high=high, low=low,
            pulse=pulse,weight=weight)
    
@app.post('/set_event')
def set_event():
    # dt = datetime.datetime.strptime(request.form.get('event_date'),"%Y-%m-%d").date()
    data = [
        request.form.get('event_name'),
        request.form.get('event_date'),
        request.form.get('discription')
    ]

    # print(request.form.get('discription'))
    ins = DB_Connector()
    ins.insert_event_data(data)
    return render_template('thanks.html')

@app.post('/finish_event')
def finish_event():
    # 受け取り側でjsonで受け取る
    # res = 'RES:' + str(request.json['id'])
    # print(res)
    res_id = request.json['id']
    res_name = Message_list.finish_event + request.json['name']
    # print(res_name)
    ins = DB_Connector()
    ins.update_event_flag(res_id)
    return '',200

@app.get('/thanks/<content>')
def show_thanks(content):
    res_name = Message_list.finish_event + content
    return render_template('thanks.html', message = res_name)

@app.get('/nav')
def show_nav():
    
    return render_template('navbar.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8000', debug=True)