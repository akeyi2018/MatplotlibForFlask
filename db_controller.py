from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from decimal import Decimal
from pytz import timezone
from sqlalchemy import case, func, cast, Integer
from werkzeug.security import generate_password_hash

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

    @classmethod
    def insert_data(cls, request):
        entry = cls(
            name=request.form.get('username'),
            mail_address=request.form.get('mail_address'),
            hash_key=generate_password_hash(request.form.get('password'), salt_length=8)
        )
        db.session.add(entry)
        db.session.commit()
        print("finish insert")

class Movie_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    episodes = db.Column(db.Integer, nullable=False, default=1)
    watched = db.Column(db.Integer, nullable=False, default=0)
    pub_date = db.Column(db.Date, nullable=False)
    genre = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.Integer, nullable=False, default=0)
    country = db.Column(db.Integer, nullable=False)
    discription = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.Integer, nullable=False, default=1)
    regist_time = db.Column(
        db.DateTime,
        default=datetime.now(timezone("Asia/Tokyo")),
    )

    @classmethod
    def get_movie_info(cls, id):
        return (
            cls.query.with_entities(
                cls.id,
                cls.title,
                m_genre.genre.label("genre"),
                m_Countries.name.label("country"),
                cls.episodes,
                cls.watched,
                cls.pub_date,
                cls.discription
            )
            .join(m_genre, m_genre.id == cls.genre)
            .join(m_Countries, m_Countries.id == cls.country)
            .filter(cls.user_id == id, cls.status == 1)
            .all()
        )

    @classmethod
    def update_movie_flag(cls, id):
        data = cls.query.filter(cls.id == id).first()
        if data:
            data.status = 0
            db.session.commit()
        else:
            print("IDがみつかりませんでした")

    @classmethod
    def insert_data(cls, request, session):
        session["id"] = 1
        data = cls.query.filter(
            cls.user_id == session["id"], cls.id == request.form.get("id")
        ).first()
        print("finish get data")
        if data:
            data.user_id = session["id"]
            data.title = request.form.get("title")
            data.episodes = request.form.get("episodes")
            data.watched = request.form.get("watched")
            data.pub_date = datetime.strptime(
                request.form.get("pub_date"), "%Y-%m-%d"
            ).date()
            data.genre = request.form.get("genre")
            data.tag = request.form.get("tag")
            data.country = request.form.get("country")
            data.discription = request.form.get("discription")
            data.rating = request.form.get("point")
            db.session.commit()
            print("finish update")
        else:
            entry = cls(
                user_id=session["id"],
                title=request.form.get("title"),
                episodes=request.form.get("episodes"),
                watched=request.form.get("watched"),
                pub_date=datetime.strptime(
                    request.form.get("pub_date"), "%Y-%m-%d"
                ).date(),
                genre=request.form.get("genre"),
                tag=request.form.get("tag"),
                country=request.form.get("country"),
                discription=request.form.get("discription"),
                rating=request.form.get("point"),
            )
            db.session.add(entry)
            db.session.commit()
            print("finish insert")


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
        tags = [
            "新機能追加",
            "機能改修",
            "バグ修正",
            "プログラム整理",
            "プロトタイプ開発",
            "メンテナンス作業",
        ]
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
        date_span = date.today() - timedelta(30)
        data_list = cls.query.filter(
            cls.user_id ==user_id, 
            cls.measure_date >= date_span
        ).all()
        measure_dates = [d.measure_date.strftime("%Y-%m-%d") for d in data_list]
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
        return (
            cls.query.with_entities(
                cls.user_id,
                cls.systolic_blood_pressure,
                cls.diastolic_blood_pressure,
                cls.weight,
            )
            .filter(cls.measure_date == date.today())
            .first()
        )

    @classmethod
    def insert_data(cls, request, session):
        session["id"] = 1
        user_id = 1
        data = cls.query.filter(
            cls.user_id == user_id, cls.measure_date == date.today()
        ).first()
        # すでに登録済の場合
        if data:
            data.user_id = int(session["id"])
            data.measure_date = date.today()
            data.systolic_blood_pressure = int(request.form.get("h_bld"))
            data.diastolic_blood_pressure = int(request.form.get("l_bld"))
            data.pulse = int(request.form.get("pulse"))
            data.weight = float(request.form.get("weight"))
            db.session.commit()
            print("finish update")
        else:
            entry = cls(
                user_id=session["id"],
                measure_date=date.today(),
                systolic_blood_pressure=request.form.get("h_bld"),
                diastolic_blood_pressure=request.form.get("l_bld"),
                pulse=request.form.get("pulse"),
                weight=request.form.get("weight"),
            )
            db.session.add(entry)
            db.session.commit()
            print("finish insert")


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

    @classmethod
    def get_event_by_id(cls, user_id, id):
        return (
            cls.query.with_entities(cls.event_name, cls.discription, cls.event_date)
            .filter(cls.id == id, cls.user_id == user_id)
            .first()
        )

    @classmethod
    def get_running_event(cls):
        return (
            cls.query.with_entities(
                cls.id,
                cls.event_name,
                cls.event_date,
                cls.discription,
                case(
                    (cls.event_date >= date.today(), "進行中"),
                    (cls.event_date < date.today(), "遅延"),
                    else_="未定義",
                ).label("status"),
                cast(
                    func.julianday(cls.event_date) - func.julianday(date.today()),
                    Integer,
                ).label("days_until_event"),
            )
            .filter(cls.finish_flag == 0)
            .order_by(cls.event_date)
            .all()
        )

    @classmethod
    def get_today_event(cls):
        # 一週間の計算
        a_week = date.today() + timedelta(7)
        return (
            cls.query.with_entities(
                cls.id,
                cls.event_name,
                cls.event_date,
                cls.discription,
                case(
                    (cls.event_date >= date.today(), "進行中"),
                    (cls.event_date < date.today(), "遅延"),
                    else_="未定義",
                ).label("status"),
                cast(
                    func.julianday(cls.event_date) - func.julianday(date.today()),
                    Integer,
                ).label("days_until_event"),
            )
            .filter(cls.finish_flag == 0, cls.event_date <= a_week)
            .order_by(cls.event_date)
            .all()
        )

    @classmethod
    def insert_data(cls, request, session):
        session["id"] = 1
        data = cls.query.filter(
            cls.user_id == session["id"], cls.id == request.form.get("event_id")
        ).first()
        print("finish get data")
        if data:
            data.event_name = request.form.get("event_name")
            data.event_date = datetime.strptime(
                request.form.get("entry_date"), "%Y-%m-%d"
            ).date()
            data.discription = request.form.get("discription")
            db.session.commit()
        else:
            entry = cls(
                user_id=session["id"],
                event_name=request.form.get("event_name"),
                event_date=datetime.strptime(
                    request.form.get("entry_date"), "%Y-%m-%d"
                ).date(),
                discription=request.form.get("discription"),
            )
            db.session.add(entry)
            db.session.commit()

    @classmethod
    def update_event_flag(cls, id):
        data = cls.query.filter(cls.id == id).first()
        if data:
            data.finish_flag = True
            db.session.commit()
        else:
            print("IDがみつかりませんでした")


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
    def get_task_by_id(cls, user_id, id):
        return (
            cls.query.with_entities(
                cls.task_name, cls.limit_date, cls.discription, cls.task_kind
            )
            .filter(cls.id == id, cls.user_id == user_id)
            .first()
        )

    @classmethod
    def update_task_flag(cls, id):
        data = cls.query.filter(cls.id == id).first()
        if data:
            data.status = False
            db.session.commit()
        else:
            print("IDがみつかりませんでした")

    @classmethod
    def get_today_task(cls):
        return (
            cls.query.with_entities(cls.id, cls.task_name, cls.discription)
            .filter(cls.status == 1, cls.limit_date <= date.today())
            .order_by(cls.limit_date)
            .all()
        )

    @classmethod
    def get_running_task(cls):
        return (
            cls.query.with_entities(
                cls.id,
                cls.task_name,
                cls.limit_date,
                cls.discription,
                m_task_tag.tag.label("tag"),
                cast(
                    func.julianday(cls.limit_date) - func.julianday(date.today()),
                    Integer,
                ).label("days_until_event"),
                case(
                    (cls.limit_date >= date.today(), "進行中"),
                    (cls.limit_date < date.today(), "遅延"),
                    else_="未定義",
                ).label("status"),
            )
            .join(m_task_tag, m_task_tag.id == cls.task_kind)
            .filter(cls.status == 1)
            .order_by(cls.limit_date)
            .all()
        )

    @classmethod
    def insert_data(cls, request, session):
        session["id"] = 1
        data = cls.query.filter(
            cls.user_id == session["id"], cls.id == request.form.get("task_id")
        ).first()
        print("finish get data")
        if data:
            data.id = request.form.get("task_id")
            data.task_name = request.form.get("task_name")
            data.limit_date = datetime.strptime(
                request.form.get("entry_date"), "%Y-%m-%d"
            ).date()
            data.discription = request.form.get("discription")
            data.task_kind = request.form.get("kind")
            db.session.commit()
            print("finish update")
        else:
            entry = cls(
                user_id=session["id"],
                task_name=request.form.get("task_name"),
                limit_date=datetime.strptime(
                    request.form.get("entry_date"), "%Y-%m-%d"
                ).date(),
                discription=request.form.get("discription"),
                task_kind=request.form.get("kind"),
            )
            db.session.add(entry)
            db.session.commit()
            print("finish insert")

class Education_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    regist_time = db.Column(
        db.DateTime,
        default=datetime.now(timezone("Asia/Tokyo")),
    )
    
    @classmethod
    def get_edu_info(cls, category_id):
        return cls.query.with_entities(
            cls.id,
            cls.title,
            cls.url
        ).filter(
            cls.category_id == category_id
        ).all()

    @classmethod
    def insert_data(cls, request, session):
        data = cls.query.filter(
            cls.id == request.form.get("id")
        ).first()
        print("finish get data")
        if data:
            data.id = request.form.get("id")
            data.category_id = request.form.get("category")
            data.title = request.form.get("title")
            data.url = request.form.get("url")
            data.status = request.form.get("status")
            db.session.commit()
            print("finish update")
        else:
            entry = cls(
                category_id = request.form.get("category"),
                title = request.form.get("title"),
                url = request.form.get("url"),
                status = request.form.get("status")
            )
            db.session.add(entry)
            db.session.commit()
            print("finish insert")

class m_Edu_Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=True, nullable=False)
    regist_time = db.Column(
        db.DateTime,
        default=datetime.now(timezone("Asia/Tokyo")),
    )
    @classmethod
    def insert_master_data(cls):
        # マスターデータを導入
        categories = [
            "Flask",
            "Game",
            "MySQL",
            "RaspberryPi",
            "Python",
            "VBA",
            "設計",
        ]
        for cate_name in categories:
            data = cls(category=cate_name)
            db.session.add(data)
        db.session.commit()

    @classmethod
    def get_category(cls, id):
        return cls.query.with_entities(
            cls.category
        ).filter(
            cls.id == id
        ).first()


class Links_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    regist_time = db.Column(
        db.DateTime,
        default=datetime.now(timezone("Asia/Tokyo")),
    )

    @classmethod
    def get_edu_info(cls, category_id):
        return cls.query.with_entities(
            cls.id,
            cls.title,
            cls.url
        ).filter(
            cls.category_id == category_id
        ).all()

    @classmethod
    def insert_data(cls, request, session):
        data = cls.query.filter(
            cls.id == request.form.get("id")
        ).first()
        print("finish get data")
        if data:
            data.id = request.form.get("id")
            data.category_id = request.form.get("category")
            data.title = request.form.get("title")
            data.url = request.form.get("url")
            data.status = request.form.get("status")
            db.session.commit()
            print("finish update")
        else:
            entry = cls(
                category_id = request.form.get("category"),
                title = request.form.get("title"),
                url = request.form.get("url"),
                status = request.form.get("status")
            )
            db.session.add(entry)
            db.session.commit()
            print("finish insert")

# class Payments(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     amount = db.Column(db.Integer)
#     item = db.Column(db.String(255))
#     date_column = db.Column(db.DateTime, default=utcnow)
#     boolean_column = db.Column(db.Boolean, default=True)
