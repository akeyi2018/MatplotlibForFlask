from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from decimal import Decimal
from pytz import timezone
from sqlalchemy import case, func, cast, Integer

db = SQLAlchemy()

# ユーザテーブル定義
class User_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regist_time = db.Column(
        db.DateTime,
        default=datetime.now(timezone("Asia/Tokyo")),
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
        countries = ["日本", "アメリカ", "中国", "韓国", "欧州", "南米"]
        for country_name in countries:
            country = cls(name=country_name)
            db.session.add(country)
        db.session.commit()


class m_genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50), unique=True, nullable=False)
    regist_time = db.Column(
        db.DateTime,
        default=datetime.now(timezone("Asia/Tokyo")),
    )

    @classmethod
    def insert_master_data(cls):
        # マスターデータを導入
        genres = ["アニメ", "国内ドラマ", "海外ドラマ", "SF", "サスペンス", "映画"]
        for genre_name in genres:
            data = cls(genre=genre_name)
            db.session.add(data)
        db.session.commit()

class m_task_tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), unique=True, nullable=False)
    regist_time = db.Column(
        db.DateTime,
        default=datetime.now(timezone("Asia/Tokyo")),
    )

    @classmethod
    def insert_master_data(cls):
        # マスターデータを導入
        tags = ["新機能追加", "機能改修", "バグ修正", "プログラム整理", "プロトタイプ開発", "メンテナンス作業"]
        for tag_name in tags:
            data = cls(tag=tag_name)
            db.session.add(data)
        db.session.commit()


class Health_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    measure_date = db.Column(db.Date, nullable=False)
    systolic_blood_pressure = db.Column(db.Integer, nullable=False)
    diastolic_blood_pressure = db.Column(db.Integer, nullable=False)
    pulse = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Numeric(5, 2), nullable=False)
    is_delete = db.Column(db.Boolean, default=False)

    @classmethod
    def get_record_by_user_id(cls, user_id):
        data_list = cls.query.filter_by(user_id=user_id).all()
        measure_dates = [d.measure_date.strftime('%Y-%m-%d') for d in data_list]
        systolic_blood_pressures = [d.systolic_blood_pressure for d in data_list]
        diastolic_blood_pressures = [d.diastolic_blood_pressure for d in data_list]
        pulses = [d.pulse for d in data_list]
        weights = [float(d.weight) for d in data_list]
        return {
            "date": measure_dates,
            "high": systolic_blood_pressures,
            "low": diastolic_blood_pressures,
            "pulse": pulses,
            "weight": weights,
        }
    
    @classmethod
    def get_today_health_info(cls):
        return cls.query.with_entities(
            cls.user_id,
            cls.systolic_blood_pressure,
            cls.diastolic_blood_pressure,
            cls.weight
        ).filter(cls.measure_date == date.today()).first()
    
    @classmethod
    def insert_data(cls, request, session):
        session["id"] = 1
        user_id = 1
        data = cls.query.filter(cls.user_id==user_id, 
                                cls.measure_date == date.today()).first()
        # すでに登録済の場合
        if data:
            data.user_id = int(session["id"])
            data.measure_date = date.today()
            data.systolic_blood_pressure=int(request.form.get("h_bld"))
            data.diastolic_blood_pressure=int(request.form.get("l_bld"))
            data.pulse=int(request.form.get("pulse"))
            data.weight=float(request.form.get("weight"))
            db.session.commit()
            print('finish update')
        else:
            entry = cls( 
                    user_id=session["id"],
                    measure_date = date.today(),
                    systolic_blood_pressure=request.form.get("h_bld"),
                    diastolic_blood_pressure=request.form.get("l_bld"),
                    pulse=request.form.get("pulse"),
                    weight=request.form.get("weight")
                )
            db.session.add(entry)
            db.session.commit()
            print('finish insert')

    # データ移行
    @classmethod
    def set_data(cls):
        # データを挿入するリスト
        data = [{'id': 2, 'user_id': 1, 'measure_date': date(2024, 2, 25), 'systolic_blood_pressure': 165, 'diastolic_blood_pressure': 121, 'pulse': 75, 'weight': Decimal('77.00')}, {'id': 3, 'user_id': 1, 'measure_date': date(2024, 2, 26), 'systolic_blood_pressure': 168, 'diastolic_blood_pressure': 119, 'pulse': 76, 'weight': Decimal('77.00')}, {'id': 4, 'user_id': 1, 'measure_date': date(2024, 2, 27), 'systolic_blood_pressure': 162, 'diastolic_blood_pressure': 119, 'pulse': 75, 'weight': Decimal('77.40')}, {'id': 5, 'user_id': 1, 'measure_date': date(2024, 2, 28), 'systolic_blood_pressure': 170, 'diastolic_blood_pressure': 120, 'pulse': 84, 'weight': Decimal('76.60')}, {'id': 6, 'user_id': 1, 'measure_date': date(2024, 2, 29), 'systolic_blood_pressure': 161, 'diastolic_blood_pressure': 120, 'pulse': 72, 'weight': Decimal('77.00')}, {'id': 7, 'user_id': 1, 'measure_date': date(2024, 3, 1), 'systolic_blood_pressure': 153, 'diastolic_blood_pressure': 112, 'pulse': 74, 'weight': Decimal('76.90')}, {'id': 8, 'user_id': 1, 'measure_date': date(2024, 3, 2), 'systolic_blood_pressure': 162, 'diastolic_blood_pressure': 110, 'pulse': 78, 'weight': Decimal('76.90')}, {'id': 9, 'user_id': 1, 'measure_date': date(2024, 3, 3), 'systolic_blood_pressure': 153, 'diastolic_blood_pressure': 112, 'pulse': 73, 'weight': Decimal('76.90')}, {'id': 10, 'user_id': 1, 'measure_date': date(2024, 3, 4), 'systolic_blood_pressure': 158, 'diastolic_blood_pressure': 114, 'pulse': 82, 'weight': Decimal('77.30')}, {'id': 11, 'user_id': 1, 'measure_date': date(2024, 3, 5), 'systolic_blood_pressure': 153, 'diastolic_blood_pressure': 112, 'pulse': 78, 'weight': Decimal('76.90')}, {'id': 12, 'user_id': 1, 'measure_date': date(2024, 3, 6), 'systolic_blood_pressure': 154, 'diastolic_blood_pressure': 112, 'pulse': 78, 'weight': Decimal('76.60')}, {'id': 13, 'user_id': 1, 'measure_date': date(2024, 3, 7), 'systolic_blood_pressure': 150, 'diastolic_blood_pressure': 108, 'pulse': 73, 'weight': Decimal('76.80')}, {'id': 14, 'user_id': 1, 'measure_date': date(2024, 3, 8), 'systolic_blood_pressure': 138, 'diastolic_blood_pressure': 106, 'pulse': 79, 'weight': Decimal('76.80')}, {'id': 15, 'user_id': 1, 'measure_date': date(2024, 3, 9), 'systolic_blood_pressure': 141, 'diastolic_blood_pressure': 101, 'pulse': 77, 'weight': Decimal('77.40')}, {'id': 16, 'user_id': 1, 'measure_date': date(2024, 3, 10), 'systolic_blood_pressure': 142, 'diastolic_blood_pressure': 105, 'pulse': 76, 'weight': Decimal('76.80')}, {'id': 17, 'user_id': 1, 'measure_date': date(2024, 3, 11), 'systolic_blood_pressure': 137, 'diastolic_blood_pressure': 108, 'pulse': 74, 'weight': Decimal('77.10')}, {'id': 18, 'user_id': 1, 'measure_date': date(2024, 3, 12), 'systolic_blood_pressure': 136, 'diastolic_blood_pressure': 103, 'pulse': 80, 'weight': Decimal('76.60')}, {'id': 23, 'user_id': 1, 'measure_date': date(2024, 3, 13), 'systolic_blood_pressure': 134, 'diastolic_blood_pressure': 98, 'pulse': 78, 'weight': Decimal('76.90')}, {'id': 24, 'user_id': 1, 'measure_date': date(2024, 3, 14), 'systolic_blood_pressure': 130, 'diastolic_blood_pressure': 98, 'pulse': 81, 'weight': Decimal('76.60')}, {'id': 25, 'user_id': 1, 'measure_date': date(2024, 3, 15), 'systolic_blood_pressure': 132, 'diastolic_blood_pressure': 98, 'pulse': 82, 'weight': Decimal('77.00')}, {'id': 26, 'user_id': 1, 'measure_date': date(2024, 3, 16), 'systolic_blood_pressure': 137, 'diastolic_blood_pressure': 101, 'pulse': 77, 'weight': Decimal('76.40')}, {'id': 28, 'user_id': 1, 'measure_date': date(2024, 3, 17), 'systolic_blood_pressure': 137, 'diastolic_blood_pressure': 101, 'pulse': 88, 'weight': Decimal('76.70')}, {'id': 29, 'user_id': 1, 'measure_date': date(2024, 3, 18), 'systolic_blood_pressure': 119, 'diastolic_blood_pressure': 95, 'pulse': 77, 'weight': Decimal('77.30')}, {'id': 30, 'user_id': 1, 'measure_date': date(2024, 3, 19), 'systolic_blood_pressure': 132, 'diastolic_blood_pressure': 100, 'pulse': 75, 'weight': Decimal('76.30')}, {'id': 31, 'user_id': 1, 'measure_date': date(2024, 3, 20), 'systolic_blood_pressure': 130, 'diastolic_blood_pressure': 96, 'pulse': 76, 'weight': Decimal('76.50')}, {'id': 32, 'user_id': 1, 'measure_date': date(2024, 3, 21), 'systolic_blood_pressure': 126, 'diastolic_blood_pressure': 96, 'pulse': 76, 'weight': Decimal('76.20')}, {'id': 33, 'user_id': 1, 'measure_date': date(2024, 3, 22), 'systolic_blood_pressure': 126, 'diastolic_blood_pressure': 96, 'pulse': 77, 'weight': Decimal('76.50')}, {'id': 34, 'user_id': 1, 'measure_date': date(2024, 3, 23), 'systolic_blood_pressure': 133, 'diastolic_blood_pressure': 93, 'pulse': 72, 'weight': Decimal('76.40')}, {'id': 35, 'user_id': 1, 'measure_date': date(2024, 3, 24), 'systolic_blood_pressure': 124, 'diastolic_blood_pressure': 97, 'pulse': 76, 'weight': Decimal('76.50')}]

        # データベースへの挿入
        for entry in data:
            health_info_entry = cls(
                id=entry['id'],
                user_id=entry['user_id'],
                measure_date=entry['measure_date'],
                systolic_blood_pressure=entry['systolic_blood_pressure'],
                diastolic_blood_pressure=entry['diastolic_blood_pressure'],
                pulse=entry['pulse'],
                weight=entry['weight']
            )
            db.session.add(health_info_entry)

        # 変更を確定
        db.session.commit()


class Event_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_name = db.Column(db.String(80), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    discription = db.Column(db.String(400), nullable=False)
    finish_flag = db.Column(db.Boolean, default=False)
    regist_time = db.Column(
        db.DateTime,
        default=datetime.now(timezone("Asia/Tokyo")),
    )

    # データ移行
    @classmethod
    def set_data(cls):
        data = [{'user_id': 1, 'event_name': '預金解約期限', 'event_date': date(2024, 5, 4), 'discription': '見直し検討'}, {'user_id': 1, 'event_name': '給料日', 'event_date': date(2024, 4, 19), 'discription': '明細確認'}, {'user_id': 1, 'event_name': 'メンター相談VBA', 'event_date': date(2024, 3, 30), 'discription': 'VBA相談 10:00から'}, {'user_id': 1, 'event_name': '箱根旅行', 'event_date': date(2024, 4, 26), 'discription': '健康保険組合保養所で宿泊'}, {'user_id': 1, 'event_name': '派遣入場', 'event_date': date(2024, 4, 2), 'discription': '入場横浜'}, {'user_id': 1, 'event_name': 'うのもり内科', 'event_date': date(2024, 4, 1), 'discription': '通院17：30'}, {'user_id': 1, 'event_name': 'iPhone返却期限', 'event_date': date(2025, 6, 30), 'discription': 'ドコモショップへ返却する'}, {'user_id': 1, 'event_name': 'お小遣い帳機能追加', 'event_date': date(2024, 3, 23), 'discription': 'お小遣い帳の追加検討'}]
        # データベースへの挿入
        for entry in data:
            event_info = cls(
                user_id=entry['user_id'],
                event_name=entry['event_name'],
                event_date=entry['event_date'],
                discription=entry['discription']
            )
            db.session.add(event_info)
        db.session.commit()

    @classmethod
    def get_running_event(cls):
        return cls.query.with_entities(
            cls.id,
            cls.event_name,
            cls.event_date,
            cls.discription,
            case(
                (cls.event_date >= date.today(), '進行中'),
                (cls.event_date < date.today(), '遅延'),
                else_='未定義'
            ).label('status'),
            cast(func.julianday(cls.event_date) - func.julianday(date.today()), Integer
            ).label('days_until_event')
        ).filter(
            cls.finish_flag == 0
        ).order_by(
            cls.event_date
        ).all()
    
    @classmethod
    def get_today_event(cls):
        return cls.query.with_entities(
            cls.id,
            cls.event_name,
            cls.event_date,
            cls.discription,
            case(
                (cls.event_date >= date.today(), '進行中'),
                (cls.event_date < date.today(), '遅延'),
                else_='未定義'
            ).label('status'),
            cast(func.julianday(cls.event_date) - func.julianday(date.today()), Integer
            ).label('days_until_event')
        ).filter(
            cls.finish_flag == 0, 
            cls.event_date<=date.today()
        ).order_by(
            cls.event_date
        ).all()

    @classmethod
    def insert_data(cls, request, session):
        session["id"] = 1
        data = cls.query.filter(
            cls.user_id==session["id"],
            cls.id == request.form.get("id")
        ).first()
        print('finish get data')
        if data:
            data.event_name = request.form.get("event_name")
            data.event_date = request.form.get("entry_date")
            data.discription = request.form.get("discription")
            db.session.commit()
        else:
            entry = cls(
                user_id = session["id"],
                event_name = request.form.get("event_name"),
                event_date = datetime.strptime(request.form.get("entry_date"), '%Y-%m-%d').date(),
                discription = request.form.get("discription")
            )
            db.session.add(entry)
            db.session.commit()

    @classmethod
    def update_event_flag(cls, id):
        data = cls.query.filter(
            cls.id == id
        ).first()
        if data:
            data.finish_flag = True
            db.session.commit()
        else:
            print('IDがみつかりませんでした')
    

class Task_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    task_name = db.Column(db.String(80), nullable=False)
    limit_date = db.Column(db.Date, nullable=False)
    discription = db.Column(db.String(800), nullable=False)
    task_kind = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    regist_time = db.Column(
        db.DateTime,
        default=datetime.now(timezone("Asia/Tokyo")),
    )

    @classmethod
    def update_task_flag(cls, id):
        data = cls.query.filter(
            cls.id == id
        ).first()
        if data:
            data.status = False
            db.session.commit()
        else:
            print('IDがみつかりませんでした')

    @classmethod
    def get_today_task(cls):
        return cls.query.with_entities(
            cls.id,
            cls.task_name,
            cls.discription
        ).filter(
            cls.status ==1, 
            cls.limit_date <= date.today()
        ).order_by(
            cls.limit_date
        ).all()

    @classmethod
    def get_running_task(cls):
        return cls.query.with_entities(
            cls.id,
            cls.task_name,
            cls.limit_date,
            cls.discription,
            m_task_tag.tag.label('tag'),
            cast(func.julianday(cls.limit_date) - func.julianday(date.today()), Integer
            ).label('days_until_event'),
            case(
                (cls.limit_date >= date.today(), '進行中'),
                (cls.limit_date < date.today(), '遅延'),
                else_='未定義'
            ).label('status')
        ).join(
            m_task_tag, m_task_tag.id == cls.task_kind
        ).filter(
            cls.status ==1
        ).order_by(
            cls.limit_date
        ).all()

    @classmethod
    def insert_data(cls, request, session):
        session["id"] = 1
        data = cls.query.filter(
            cls.user_id==session["id"],
            cls.id == request.form.get("id")
        ).first()
        print('finish get data')
        if data:
            data.id = request.form.get("task_id")
            data.user_id = int(session["id"])
            data.task_name = request.form.get("task_name")
            data.limit_date = request.form.get("entry_date")
            data.discription = request.form.get("discription")
            data.task_kind = request.form.get("kind")
            db.session.commit()
            print('finish update')
        else:
            entry = cls(
                user_id=session["id"],
                task_name = request.form.get("task_name"),
                limit_date = datetime.strptime(request.form.get("entry_date"), '%Y-%m-%d').date(),
                discription = request.form.get("discription"),
                task_kind = request.form.get("kind")
            )
            db.session.add(entry)
            db.session.commit()
            print('finish insert')


# class Payments(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     amount = db.Column(db.Integer)
#     item = db.Column(db.String(255))
#     date_column = db.Column(db.DateTime, default=utcnow)
#     boolean_column = db.Column(db.Boolean, default=True)
