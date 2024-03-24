from sqlalchemy import text
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from db_controller import db
from sqlalchemy.exc import ProgrammingError


class Event_view_running(db.Model):
    __tablename__ = 'view_event_running'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_name = db.Column(db.String(80), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    discription = db.Column(db.String(400), nullable=False)
    left_days = db.Column(db.Integer, default=False)
    status = db.Column(db.String(10), nullable=False)

    @classmethod
    def create_view(cls):
        drop_view_sql = text('DROP VIEW view_event_running;')
        create_view_sql = text('''
        CREATE VIEW view_event_running AS
        SELECT id, user_id, event_name, event_date, discription, 
        CAST(JULIANDAY(event_date) - JULIANDAY('now') AS INTEGER) as left_days,
        CASE WHEN JULIANDAY(event_date) - JULIANDAY('now') >= 0 THEN '進行中'
        WHEN JULIANDAY(event_date) - JULIANDAY('now') < 0 THEN '遅延' 
        ELSE '未定義'
        END AS status
        FROM event_info
        ''')
        with current_app.app_context():
            try:
                db.session.execute(drop_view_sql)
            except ProgrammingError:
                pass  # ビューが存在しない場合は何もしない
            db.session.execute(create_view_sql)
            db.session.commit()
