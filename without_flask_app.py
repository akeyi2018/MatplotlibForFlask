from flask_sqlalchemy import SQLAlchemy
from db_controller import Event_info, db
from flask import Flask
import os
from send_mail import pymail
from datetime import date

# 仮想のFlaskアプリケーションコンテキストを作成します。
class DummyApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config.update({
            'SQLALCHEMY_DATABASE_URI': "sqlite:///" + os.path.join(
            os.getcwd(), "settings", "health_db.db"),
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        })

# Flask-SQLAlchemyを初期化します。
def initialize_sqlalchemy(app):
    db.init_app(app)

def clean_data(data):
    result = ''
    for d in data:
        # print(d.event_date)
        tmp = '【' + d.event_date.strftime("%Y-%m-%d") + '】\n【' + d.event_name + '】\n【' + d.discription +'】\n\n'
        result = result+tmp
    return result 


# データベースに接続します。
def connect_to_database():
    app = DummyApp(__name__)
    initialize_sqlalchemy(app)
    with app.app_context():
        db.create_all()
        # ここでデータベースを使用した操作を行います。
        res = Event_info.get_today_event()
        r = clean_data(res)
        ins = pymail()
        dt = date.today().strftime("%Y-%m-%d")
        ins.send_mail(f'【{dt}】のイベント情報:', r)


# データベースに接続します。
connect_to_database()
