# -*- coding: utf-8 -*-
from flask import (
    Flask,  #Flask本体
    render_template, #HTMLレンダリングエンジン
    request,   #POSTの戻り値の受け取り用
    send_from_directory, #Front側に参照フォルダを送信する
    session, #ログイン用セッション
    redirect, #リダイレクト
    url_for
)
from flask_bootstrap import Bootstrap
import datetime
from werkzeug.security import generate_password_hash
import os
from pytz import timezone
import flask_login

# 自作クラス
from mysql_tool import DB_Connector
from settings import Message_list, Sql_Param
from form_list import LoginForm, RegistUserForm
from admin_user import AdminUser

login_manager = flask_login.LoginManager()
app = Flask(__name__, static_folder='./static')
app.config['SECRET_KEY'] = Sql_Param.KEY
login_manager.init_app(app)
login_manager.login_view = 'login'

bootstrap = Bootstrap(app)

# ユーザ情報ロード
@login_manager.user_loader
def load_user(user_id):
    return AdminUser(user_id)

# ログインフォーム
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 登録ユーザかどうかの認証
        username = form.username.data
        ins = DB_Connector()
        user_id = ins.get_user_id(username)

        # sessionは自由に登録できる
        session['user_name'] = user_id['name']
        session['id'] = user_id['id']
        session['flag'] = True

        # AdminUserに登録しておく
        user_id = AdminUser(user_id=user_id)
        # flask_loinで認識できる形で登録する
        flask_login.login_user(user_id)
       
        return redirect(url_for('index'))
    else:
        return render_template('login.html', form=form)

@app.route('/')
def main():
    return render_template('main.html')

def set_nav_info():
    return [{
            "text": "Dashboard",
            "id": "v-pills-dashboard",
            "label": "v-pills-dashboard-tab",
            "url": "dashboard.html"
        },
        {
            "text": "血圧体重管理",
            "id": "v-pills-messages",
            "label": "v-pills-messages-tab",
            "url": "bodyweight_graph.html"
        },
        {
            "text": "profile",
            "id": "v-pills-profile",
            "label": "v-pills-profile-tab",
            "url": "profile.html"
        },
        {
            "text": "スケジュール管理",
            "id": "v-pills-schedule",
            "label": "v-pills-schedule-tab",
            "url": "regist_event.html"
        }
    ]

@app.route('/home')
@flask_login.login_required
def index():
    # session check
    if not session.get('flag') is None:
        ins = DB_Connector()
        session['id'] = 1 # 暫定的に1にする完成時は不要
        data = ins.sharpe_data_to_graph(session['id'])
        # データ入力フラグ
        flag = ins.check_date(datetime.date.today().strftime("%Y-%m-%d"))
        event_data = ins.get_event_data(1)
        user_name = session['user_name']

        return render_template('index.html',
                            health_data=data, 
                            flag=flag, 
                            event_data= event_data, 
                            user=user_name, nav=set_nav_info())
    # ログインページへ誘導
    return redirect(url_for('main'))
    
@app.route('/regist_user', methods=['GET','POST'])
def regist_public_user():
    form = RegistUserForm()
    if form.validate_on_submit():
        data = {
            "regist_time": datetime.datetime.now(timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S"),
            "name": form.username.data,
            "mail_address": form.mail_address.data,
            "hash_key": generate_password_hash(form.password.data, salt_length=8)
        }
        # ユーザ登録
        ins = DB_Connector()
        ins.insert_data('user_info', data)
        return redirect(url_for('show_thanks', content=Message_list.user_regist_event))

    # ユーザ登録フォームの表示
    return render_template('admin_regist.html', form=form) 

@app.get('/profile')
@flask_login.login_required
def show_profile():
    return render_template('profile.html')

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
@flask_login.login_required
def set_event():
    data = [
        request.form.get('event_name'),
        request.form.get('event_date'),
        request.form.get('discription')
    ]

    ins = DB_Connector()
    ins.insert_event_data(data)
    return render_template('thanks.html')

@app.post('/finish_event')
@flask_login.login_required
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

@app.route('/logout')
def logout():
    session.pop('flag',None)
    session.pop('username',None)
    return redirect(url_for('main'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8000', debug=True)