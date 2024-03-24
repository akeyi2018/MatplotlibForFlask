from sqlalchemy import text
from flask import current_app
from db_controller import db

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
    def create_table(cls):
        create_table_sql = text('''
        CREATE TABLE IF NOT EXISTS view_event_running (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            event_name VARCHAR(80) NOT NULL,
            event_date DATE NOT NULL,
            discription VARCHAR(400) NOT NULL,
            left_days INTEGER DEFAULT 0,
            status VARCHAR(10) NOT NULL
        );
        ''')
        with current_app.app_context():
            try:
                db.session.execute(create_table_sql)
                db.session.commit()
                print("Table created successfully.")
            except Exception as e:
                print("Error creating table:", str(e))
                db.session.rollback()

    @classmethod
    def refresh_data(cls):
        create_table_sql = text('''
        CREATE OR REPLACE VIEW view_event_running AS
        SELECT id, user_id, event_name, event_date, discription, 
        CAST(JULIANDAY(event_date) - JULIANDAY('now') AS INTEGER) as left_days,
        CASE WHEN JULIANDAY(event_date) - JULIANDAY('now') >= 0 THEN '進行中'
        WHEN JULIANDAY(event_date) - JULIANDAY('now') < 0 THEN '遅延' 
        ELSE '未定義'
        END AS status
        FROM event_info
        WHERE finish_flag = 1
        ''')
        with current_app.app_context():
            try:
                db.session.execute(create_table_sql)
                db.session.commit()
                print("Table created successfully.")
            except Exception as e:
                print("Error creating table:", str(e))
                db.session.rollback()

