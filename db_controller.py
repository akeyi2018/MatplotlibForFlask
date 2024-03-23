from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone

db = SQLAlchemy()


class User_info(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    regist_time = db.Column(
        db.DateTime,
        default=datetime.now(timezone("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S"),
    )
    name = db.Column(db.String(100), nullable=False)
    mail_address = db.Column(db.String(255), unique=True, nullable=False)
    hash_key = db.Column(db.String(255), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=True)

# 国マスター
class m_Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    regist_time = db.Column(
        db.DateTime,
        default=datetime.now(timezone("Asia/Tokyo")),
    )

    @classmethod
    def insert_master_data(cls):
        # マスターデータを導入
        countries = ['日本', 'アメリカ', '中国', '韓国', '欧州', '南米']
        for country_name in countries:
            country = cls(name=country_name)
            db.session.add(country)
        db.session.commit()

# class Payments(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     amount = db.Column(db.Integer)
#     item = db.Column(db.String(255))
#     date_column = db.Column(db.DateTime, default=datetime.utcnow)
#     boolean_column = db.Column(db.Boolean, default=True)