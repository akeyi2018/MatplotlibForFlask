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
from waitress import serve

# 自作クラス
from mysql_tool import DB_Connector
from settings import Message_list, Sql_Param, Html_Param
from form_list import (LoginForm, 
                       RegistUserForm, 
                       RegistTaskForm, 
                       RegistEventForm,
                       RegistTVForm,
                       RegistHealthForm,
)
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

@app.route('/')
def main():
    return render_template('main.html')

#region -----登録------
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

@app.post('/confirm')
def confirm_data():
    # 健康データ入力処理
    Html_Param.insert_health_info(request, session)
    return render_template('thanks.html')

#endregion

#region ------GET----------
@app.get('/regist_tv_info/<id>')
@flask_login.login_required
def show_regist_tv_info(id):
    id = int(id)
    if id ==0:
        form = RegistTVForm(id=id)
    else:
        pass
    return render_template('regist_tv_info.html', tform = form)

@app.get('/profile')
@flask_login.login_required
def show_profile():
    return render_template('profile.html')

@app.get('/line')
@flask_login.login_required
def show_linear():
    return render_template('weight.html')

@app.get('/regist_health')
@flask_login.login_required
def regist_health_info():
    form = RegistHealthForm()
    return render_template('regist_health.html', form=form)

# 新規登録と編集で初期設定するパラメータが変わる為、関数で振り分けしている
@app.get('/show_task/<id>')
@flask_login.login_required
def show_task(id):
    id = int(id)
    if id ==0: # 新規登録
        form = RegistTaskForm()
    else: # 編集 既存の情報を取得する
        ins = DB_Connector()
        task_info = ins.get_task_view_by_id(int(session['id']), id)
        form = RegistTaskForm(task_id=id,
                            task_name = task_info['task_name'],
                            discription=task_info['detail'],
                            entry_date=task_info['limit_date'],
                            kind=99,
                            choice = "更新"
                            )
    return render_template('regist_task.html', tform=form)

@app.get('/edit_tv_info/<id>')
@flask_login.login_required
def edit_tv_info(id):
    id = int(id)
    if id ==0: # 新規登録
        form = RegistTVForm()
    else: # 編集 既存の情報を取得する
        ins = DB_Connector()
        tv_info = ins.get_tv_info_by_id(int(session['id']), id)
        print(tv_info)
        form = RegistTVForm(id=id,
                            title = tv_info['title'],
                            episodes = tv_info['episodes'],
                            watched = tv_info['watched'],
                            pub_date=tv_info['pub_date'],
                            genre = tv_info['genre'],
                            country = tv_info['country'],
                            discription=tv_info['discription'],
                            tag = tv_info['tag'],
                            point = tv_info['point'],
                            choice = 1
                            )
    return render_template('regist_tv_info.html', tform=form)

@app.get('/show_event/<id>')
@flask_login.login_required
def show_event(id):
    id = int(id)
    if id ==0:
        form = RegistEventForm()
    else:
        # idがゼロでない場合は、既存の情報を取得する
        ins = DB_Connector()
        event_info = ins.get_event_view_by_id(int(session['id']), id)
        form = RegistEventForm(event_id=id,
                            event_name = event_info['event_name'],
                            discription=event_info['discription'],
                            entry_date=event_info['event_date'],
                            kind=99,
                            choice = "更新"
                            )
    return render_template('regist_event.html', eform=form)

@app.get('/thanks/<kind>/<content>')
def show_thanks(kind, content):
    kind = int(kind)
    if kind == 0:
        res_name = Message_list.finish_event + content
    elif kind == 1:
        res_name = Message_list.finish_task + content
    elif kind == 2:
        res_name = Message_list.finish_tv + content
    return render_template('thanks.html', message = res_name)

@app.get('/nav')
def show_nav():
    return render_template('navbar.html')

@app.get('/gauge')
def show_gauge():
    return render_template('gauge_chart.html')

@app.get('/logout')
def logout():
    session.pop('flag',None)
    session.pop('username',None)
    return redirect(url_for('main'))

@app.get('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#endregion

#region ------POST----------
@app.post('/set_tv_info')
@flask_login.login_required
def set_tv_info():
    Html_Param.insert_tv_info(request, session)
    return render_template('thanks.html')

@app.post('/set_event')
@flask_login.login_required
def set_event():
    Html_Param.insert_event_info(request, session)
    return render_template('thanks.html')

@app.post('/set_task')
@flask_login.login_required
def set_task():
    Html_Param.insert_task_info(request, session)
    return render_template('thanks.html')

@app.post('/finish_event')
@flask_login.login_required
def finish_event():
    # 受け取り側でjsonで受け取る
    ins = DB_Connector()
    ins.update_event_flag(request.json['id'])
    return '',200

@app.post('/finish_tv')
@flask_login.login_required
def finish_tv():
    # 受け取り側でjsonで受け取る
    ins = DB_Connector()
    ins.update_tv_flag(request.json['id'])

    return '',200

@app.post('/finish_task')
@flask_login.login_required
def finish_task():

    from push_source_to_github import push_git

    # 受け取り側でjsonで受け取る
    # res = 'RES:' + str(request.json['id'])
    res_id = request.json['id']
    res_content = request.json['name']
    # print(res_id)
    ins = DB_Connector()
    ins.update_task_flag(res_id)

    # githubに自動push
    p = push_git()
    p.shell_cmd(res_id, res_content)

    return '',200
#endregion

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

# ホーム
@app.route('/home')
@flask_login.login_required
def index():
    # session check
    if not session.get('flag') is None:
        return render_template(
            'index.html',
            home = Html_Param.func_home(session),
            nav=Html_Param.nav_home
        )
    # ログインページへ誘導
    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8000', debug=True)
    # serve(app, host='0.0.0.0', port=5000)