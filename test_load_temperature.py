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


def get_data():
    app = DummyApp(__name__)
    initialize_sqlalchemy(app)

    with app.app_context():
        db.create_all()
        data_list = Environment_info.get_latest()
        for data in data_list:
            # formatted_time = data.timestamp.strftime("%Y-%m-%d %H:%M")
            # print(data.timestamp, data.temperature, data.humidity)


get_data()

