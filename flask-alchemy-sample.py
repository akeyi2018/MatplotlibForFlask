from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# 自作クラス
from settings import Sql_Param
from al_admin_user import User_info
from al_admin_user import db as user_info_tbl

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'settings', 'payments_db.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db_uri = f'mysql+pymysql://{Sql_Param.user}:{Sql_Param.passwd}@{Sql_Param.host}/{Sql_Param.alchemy_database}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# user_infoテーブル初期化
user_info_tbl.init_app(app)

# class Payments(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     amount = db.Column(db.Integer)
#     item = db.Column(db.String(255))
#     date_column = db.Column(db.DateTime, default=datetime.utcnow)
#     boolean_column = db.Column(db.Boolean, default=True)

@app.route('/')
def main():
    with app.app_context():
        user_info_tbl.create_all() # テーブル作成

    # user = User(username='john2', email='john2@example.com')
    # db.session.add(user)
    # db.session.commit()
        
    # pay = Payments(user_id=2, amount=100, item='ジュース')
    # db.session.add(pay)
    # db.session.commit()
    return 'Hello', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000', debug=True)
