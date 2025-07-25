# -*- coding: utf-8 -*-
from flask import (
    Flask,  # Flask本体
    render_template,  # HTMLレンダリングエンジン
    request,  # POSTの戻り値の受け取り用
    session,  # ログイン用セッション
    redirect,  # リダイレクト
    url_for,
)
from flask_bootstrap import Bootstrap
import flask_login


# 自作クラス
import form_settings
from settings import Sql_Param
from db_controller import db as user_info_tbl

from db_controller import (
    User_info,
    m_Countries,
    m_genre,
    m_task_tag,
    Health_info,
    Event_info,
    Task_info,
    Movie_info,
    Education_info,
    Links_info,
    m_Edu_Categories,
)
from settings import Message_list, Sql_Param, Html_Param
from form_list import (
    LoginForm,
    RegistUserForm,
    RegistHealthForm,
)
from admin_user import AdminUser

from initialization import initialize_app

# region ----------------- INIT ---------------------
# ログインマネージャーの宣言
login_manager = flask_login.LoginManager()

# 初期に読ませるフォルダを./staticにセットする
app = Flask(__name__, static_folder="./static")

# 初期化
app = initialize_app(app)

# loginマネージャーとFlaskを統合
login_manager.init_app(app)
# 要検証
login_manager.login_view = "login"

# user_infoテーブル初期化
user_info_tbl.init_app(app)

# bootstrapを使えるようにする
bootstrap = Bootstrap(app)


# ユーザ情報ロード
@login_manager.user_loader
def load_user(user_id):
    return AdminUser(user_id)


# endregion


# region -----登録------
@app.route("/regist_user", methods=["GET", "POST"])
def regist_public_user():  # Adminユーザの登録
    form = RegistUserForm()
    if form.validate_on_submit():
        # 登録するユーザ情報を作成する
        User_info.insert_data(request)

        return redirect(
            url_for("show_thanks", kind=3, content=Message_list.user_regist_event)
        )

    # ユーザ登録フォームの表示
    return render_template("admin_regist.html", form=form)


@app.post("/confirm")
def confirm_data():
    # 健康データ入力処理
    Health_info.insert_data(request, session)
    return render_template("thanks.html")

# endregion


# region ------GET----------
@app.get("/education/<id>")
@flask_login.login_required
def show_education(id):
    id = int(id)
    category, nav = Html_Param.get_nav_info(id)
    return render_template('education.html', category=category, nav = nav)

@app.get("/regist_health")
@flask_login.login_required
def regist_health_info():
    form = RegistHealthForm()
    latest_data = Health_info.get_today_health_info()
    if latest_data:
        form.h_bld.data = latest_data.systolic_blood_pressure
        form.l_bld.data = latest_data.diastolic_blood_pressure
    return render_template("regist_health.html", form=form)

@app.get("/thanks/<kind>/<content>")
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
    return render_template("thanks.html", message=res_name)


@app.get("/edit_event/<id>")
@flask_login.login_required
def edit_event(id):
    return render_template(
        "regist_event.html", eform=form_settings.set_event_form(id, session)
    )


@app.get("/edit_task/<id>")
@flask_login.login_required
def edit_task(id):
    return render_template(
        "regist_task.html", tform=form_settings.set_task_form(id, session)
    )


@app.get("/edit_tv_info/<id>")
@flask_login.login_required
def edit_tv_info(id):
    return render_template(
        "regist_tv_info.html", tform=form_settings.set_tv_form(id, session)
    )

@app.get("/edit_edu_info/<id>")
@flask_login.login_required
def edit_edu_info(id):
    return render_template(
        "regist_edu_info.html", form=form_settings.set_edu_form(id, session)
    )

@app.get("/edit_link_info/<id>")
@flask_login.login_required
def edit_link_info(id):
    return render_template(
        "regist_link_info.html", form=form_settings.set_link_form(id, session)
    )

@app.get("/show_link")
@flask_login.login_required
def show_links():
    links_info, pagenation = Html_Param.get_link_pagination()
    home= {
        "link_info": links_info,
        "pagenation": pagenation,
    }
    return render_template(
        "link.html", home=home
    )

# endregion


# region ------POST----------
@app.post("/set_tv_info")
@flask_login.login_required
def set_tv_info():
    Movie_info.insert_data(request, session)
    regist_link = 'edit_tv_info'
    link_text = '続けてテレビ映画情報を登録する'
    return render_template("thanks.html", regist_link=regist_link, link_text=link_text)


@app.post("/set_edu_info")
@flask_login.login_required
def set_edu_info():
    Education_info.insert_data(request, session)
    regist_link = 'edit_edu_info'
    link_text = '続けて教材を登録する'
    return render_template("thanks.html", regist_link=regist_link, link_text=link_text)

@app.post("/set_link_info")
@flask_login.login_required
def set_link_info():
    Links_info.insert_data(request, session)
    regist_link = 'edit_link_info'
    link_text = '続けてリンクを登録する'
    return render_template("thanks.html", regist_link=regist_link, link_text=link_text)


@app.post("/set_task")
@flask_login.login_required
def set_task():
    Task_info.insert_data(request, session)
    regist_link = 'edit_task'
    link_text = '続けてタスクを登録する'
    return render_template("thanks.html", regist_link=regist_link, link_text=link_text)


@app.post("/set_event")
@flask_login.login_required
def set_event():
    Event_info.insert_data(request, session)
    regist_link = 'edit_event'
    link_text = '続けてイベントを登録する'
    return render_template("thanks.html", regist_link=regist_link, link_text=link_text)


# endregion


# region ==========PUT==============
@app.put("/finish_tv")
@flask_login.login_required
def finish_tv():
    # 受け取り側でjsonで受け取る
    Movie_info.update_movie_flag(request.json["id"])
    return "", 200


@app.put("/finish_event")
@flask_login.login_required
def finish_event():
    # 受け取り側でjsonで受け取る
    Event_info.update_event_flag(request.json["id"])
    return "", 200


@app.put("/finish_task")
@flask_login.login_required
def finish_task():

    res_id = request.json["id"]

    Task_info.update_task_flag(res_id)

    return "", 200

@app.put("/finish_task_push")
@flask_login.login_required
def finish_task_push():

    from push_source_to_github import push_git

    res_id = request.json["id"]

    Task_info.update_task_flag(res_id)

    # githubに自動push
    p = push_git()
    p.shell_cmd(res_id, request.json["name"])

    return "", 200


# endregion


# region --------MAIN----------
@app.route("/")
def main():

    # 初期化作業
    with app.app_context():
        user_info_tbl.create_all()  # テーブル作成

    if Sql_Param.debug_flag == True:
        m_Countries.insert_master_data()  # 国マスターデータの投入
        m_genre.insert_master_data()  # ジャンルマスターデータの投入
        m_task_tag.insert_master_data()
        m_Edu_Categories.insert_master_data()

        print("マスター初期化完了")

    return render_template("main.html")


# ログインフォーム
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 登録ユーザかどうかの認証
        username = form.username.data
        user_id = User_info.query.filter_by(mail_address=username).first()
        # print(user_id.name)
        if user_id:
            # sessionは自由に登録できる
            session["user_name"] = user_id.name
            session["id"] = user_id.id
            session["flag"] = True

            # AdminUserに登録しておく
            user_id = AdminUser(user_id=user_id.id)
            # flask_loinで認識できる形で登録する
            flask_login.login_user(user_id)

            return redirect(url_for("index"))
    return render_template("login.html", form=form)


# ホーム
@app.route("/home", methods=['GET','POST'])
@flask_login.login_required
def index():
    # session check
    if not session.get("flag") is None:
        return render_template(
            "index.html",
            home=Html_Param.get_home_data(session),
            nav=Html_Param.nav_home,
        )
    # ログインページへ誘導
    return redirect(url_for("main"))


@app.get("/logout")
def logout():
    session.pop("flag", None)
    session.pop("username", None)
    return redirect(url_for("main"))


# endregion

if __name__ == "__main__":
    if Sql_Param.release_flag == '0':
        app.run(host="0.0.0.0", port="5001", debug=True)
    else:
        app.run(host="0.0.0.0", port="5000", debug=False)
