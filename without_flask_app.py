#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from db_controller import Event_info, Environment_info, db
from flask import Flask
import os
from send_mail import pymail
from datetime import date
import schedule
from temp_humid import TemperatureSensor
import time
from udp_8_band import Udp_server_led

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


def save_environment_data():
    app = DummyApp(__name__)
    initialize_sqlalchemy(app)

    with app.app_context():
        sensor = TemperatureSensor(sensor_model='DHT11')
        sensor.read()
        if sensor.pre_temp is not None and sensor.pre_humid is not None:
            Environment_info.insert_data(sensor.pre_temp, sensor.pre_humid) 

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
        if not res:
            r = 'イベントの予定はありません。'
        else:
            r = clean_data(res)
            ins = pymail()
            dt = date.today().strftime("%Y-%m-%d")
            ins.send_mail(f'【{dt}】のイベント情報:', r)

def run_led():
    udp_server = Udp_server_led()
    udp_server.run()

schedule.every().day.at("06:55").do(connect_to_database)
schedule.every().hour.at(":00").do(save_environment_data)

# schedule.every(1).minutes.do(save_environment_data)

# run_led()

# データベースに接続します。
# connect_to_database()
# save_environment_data()

while True:
    schedule.run_pending()
    time.sleep(1)
