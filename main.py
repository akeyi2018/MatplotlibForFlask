# -*- coding: utf-8 -*-
from flask import (
    Flask,  # Flask本体
    render_template,  # HTMLレンダリングエンジン
    request,  # POSTの戻り値の受け取り用
    send_from_directory,  # Front側に参照フォルダを送信する
    session,  # ログイン用セッション
    redirect,  # リダイレクト
    url_for,
)
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

# 自作クラス
from settings import Sql_Param
from db_controller import User_info, m_Countries, m_genre
from db_controller import db as user_info_tbl
from settings import Message_list, Sql_Param, Html_Param
from form_list import (
    LoginForm,
    RegistUserForm,
    RegistTaskForm,
    RegistEventForm,
    RegistTVForm,
    RegistHealthForm,
)

# 初期に読ませるフォルダを./staticにセットする
app = Flask(__name__, static_folder='./static')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    os.getcwd(), "settings", "health_db.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# CSRF 認証キーのセット
app.config['SECRET_KEY'] = Sql_Param.KEY

# db_uri = f'mysql+pymysql://{Sql_Param.user}:{Sql_Param.passwd}@{Sql_Param.host}/{Sql_Param.alchemy_database}'
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# user_infoテーブル初期化
user_info_tbl.init_app(app)

# bootstrapを使えるようにする
bootstrap = Bootstrap(app)


# region -----登録------
@app.route("/regist_user", methods=["GET", "POST"])
def regist_public_user():
    form = RegistUserForm()
    if form.validate_on_submit():
        # 登録するユーザ情報を作成する
        user = User_info(name=form.username.data, 
                         mail_address=form.mail_address.data,
                         hash_key=generate_password_hash(form.password.data, salt_length=8)
            )
        # テーブルにデータを登録する
        user_info_tbl.session.add(user)
        user_info_tbl.session.commit()
        

        # data = {
        #     "regist_time": datetime.datetime.now(timezone("Asia/Tokyo")).strftime(
        #         "%Y-%m-%d %H:%M:%S"
        #     ),
        #     "name": form.username.data,
        #     "mail_address": form.mail_address.data,
        #     "hash_key": generate_password_hash(form.password.data, salt_length=8),
        # }
        # # ユーザ登録
        # ins = DB_Connector()
        # ins.insert_data("user_info", data)
        return redirect(url_for("show_thanks", kind=3, content=Message_list.user_regist_event))

    # ユーザ登録フォームの表示
    return render_template("admin_regist.html", form=form)


# endregion

#region ------GET----------
@app.get('/thanks/<kind>/<content>')
def show_thanks(kind, content):
    kind = int(kind)
    if kind == 0:
        res_name = Message_list.finish_event + content
    elif kind == 1:
        res_name = Message_list.finish_task + content
    elif kind == 2:
        res_name = Message_list.finish_tv + content
    elif kind == 3:
        res_name = Message_list.user_regist_event
    return render_template('thanks.html', message = res_name)

#endregion

@app.route("/")
def main():

    # 初期化作業
    with app.app_context():
        user_info_tbl.create_all()  # テーブル作成

    if Sql_Param.debug_flag == True:
        m_Countries.insert_master_data()  # 国マスターデータの投入
        m_genre.insert_master_data()  # ジャンルマスターデータの投入

        print("マスター初期化完了")



    # pay = Payments(user_id=2, amount=100, item='ジュース')
    # db.session.add(pay)
    # db.session.commit()
    # return "Hello", 200
    return render_template('main.html')

# ログインフォーム
@app.route('/login', methods=['GET','POST'])
def login():
    return "Login", 200

# ホーム
@app.route('/home')
# @flask_login.login_required
def index():
    # session check
    # if not session.get('flag') is None:
    #     return render_template(
    #         'index.html',
    #         home = Html_Param.func_home(session),
    #         nav=Html_Param.nav_home
    #     )
    # ログインページへ誘導
    return redirect(url_for('main'))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
