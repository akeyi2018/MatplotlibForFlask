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
import locale
from werkzeug.security import generate_password_hash
import os
from pytz import timezone
import flask_login

# 自作クラス
from mysql_tool import DB_Connector
from settings import Message_list, Sql_Param, Html_Param
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

@app.route('/home')
@flask_login.login_required
def index():
    # session check
    if not session.get('flag') is None:
        # 日本語で曜日の表示
        locale.setlocale(locale.LC_ALL, '')
        dt = datetime.date.today()
        ins = DB_Connector()
        session['id'] = 1 # 暫定的に1にする完成時は不要
        data = ins.sharpe_data_to_graph(session['id'])
        
        view_today = dt.strftime("%Y年%m月%d日（%A）")
        view_day = dt.strftime("%m月%d日(%a)")
        # 健康データの取得
        health_info = ins.get_today_health(session['id'])
        health_info_goal = ins.get_goal_health(session['id'])
        health_info_diff = ins.get_diff_health(session['id'])

        event_data = ins.get_today_event(session['id'])
        
        task_data = ins.get_today_task(session['id'])
        user_name = session['user_name']

        return render_template('index.html',
                            health_data=data, 
                            dt = view_today,
                            dt2 = view_day,
                            health_info = health_info,
                            health_info_goal = health_info_goal,
                            health_info_diff = health_info_diff,
                            event_data = event_data,
                            task_data = task_data, 
                            user = user_name, 
                            nav=Html_Param.nav_home,
                            task=Html_Param.task_home)
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

@app.get('/regist_health')
@flask_login.login_required
def regist_health_info():
    return render_template('regist_health.html')

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

@app.post('/set_task')
@flask_login.login_required
def set_task():
    # session['id']
    # 種類の大文字、間違いを対応
    try:
        kind = int(request.form.get('task_category'))
    except:
        kind = 1

    data = {
        "user_id": 1,
        "task_name": request.form.get('task_name'),
        "detail": request.form.get('discription'),
        "limit_date": request.form.get('task_limit_date'),
        "task_kind": kind,
        "status": 1,
        "regist_date": datetime.datetime.now(timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")
    }

    ins = DB_Connector()
    ins.insert_data('task_info', data)

    return render_template('thanks.html')

@app.post('/finish_event')
@flask_login.login_required
def finish_event():
    # 受け取り側でjsonで受け取る
    # res = 'RES:' + str(request.json['id'])
    res_id = request.json['id']
    ins = DB_Connector()
    ins.update_event_flag(res_id)
    return '',200

@app.post('/finish_task')
@flask_login.login_required
def finish_task():
    # 受け取り側でjsonで受け取る
    # res = 'RES:' + str(request.json['id'])
    res_id = request.json['id']
    # print(res_id)
    ins = DB_Connector()
    ins.update_task_flag(res_id)
    return '',200

@app.get('/thanks/<kind>/<content>')
def show_thanks(kind, content):
    if int(kind) == 0:
        res_name = Message_list.finish_event + content
    elif int(kind) == 1:
        res_name = Message_list.finish_task + content
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