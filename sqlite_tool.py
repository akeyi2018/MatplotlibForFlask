from datetime import datetime
import sqlite3
from pytz import timezone
import os, json


class SQLiteConnector:
    def __init__(self) -> None:
        try:
            self.SQLALCHEMY_DATABASE_URI = os.path.join(os.getcwd(),'settings','payments_db.db')
            self.connection = sqlite3.connect(self.SQLALCHEMY_DATABASE_URI)
            self.curs = self.connection.cursor()
            print(self.curs)
        except Exception as e:
            print(f'Error Occurred: {e}')
    
    def insert_public_user(self, data):
        sql = "INSERT INTO user_info (regist_time, name, mail_address, hash_key) VALUES \
            (%s, %s, %s, %s)"
        values = [datetime.now(timezone('Asia/Tokyo'))] + data
        self.curs.execute(sql, values)
        self.connector.commit()

    def get_user_id(self, username):
        sql = 'SELECT id, name, hash_key FROM user_info WHERE mail_address=%s LIMIT 1'
        values = (username,)
        self.curs.execute(sql, values)
        return self.curs.fetchone()

    def insert_health_data(self, data):
        if self.check_date(data=data[0]):
            sql = "INSERT INTO health_info \
                (user_id, measure_date, \
                systolic_blood_pressure, diastolic_blood_pressure, \
                pulse, weight, create_time) VALUES \
                (%s, %s, %s, %s, %s, %s, %s) "
            value1 = [1]
            value2 = [datetime.now(timezone('Asia/Tokyo'))]
            values = value1 + data + value2
            self.curs.execute(sql, values)
            self.connector.commit()

    def insert_data(self, table_name, json_data):
        # JSONデータをパースしてカラム名とデータを取得する
        # print(json_data)
        data_dict = json.loads(json.dumps(json_data))
        
        columns = list(data_dict.keys())
        data = list(data_dict.values())

        # カラム名をSQLクエリに挿入する部分を動的に生成する
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(data))
        
        # SQLクエリを構築する
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        
        # イベントデータを挿入する値を作成する
        values = data
        
        # クエリを実行してコミットする
        self.curs.execute(sql, values)
        self.connector.commit()

    def update_data(self, table_name, json_data, condition_json_data):
        # JSONデータをパースしてカラム名とデータを取得する
        data_dict = json.loads(json.dumps(json_data))
        set_clause = ', '.join([f"{key} = %s" for key in data_dict.keys()])
        values = list(data_dict.values())

        # 条件JSONデータをパースして条件値を取得する
        condition_dict = json.loads(json.dumps(condition_json_data))

        # 条件値を追加する
        values.extend(list(condition_dict.values()))

        # 条件カラムを取得する
        condition_columns = list(condition_dict.keys())

        # SQLクエリを構築する
        condition_str = " AND ".join([f"{column} = %s" for column in condition_columns])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition_str}"

        # クエリを実行してコミットする
        self.curs.execute(sql, values)
        self.connector.commit()

    def update_event_flag(self, event_id):
        sql = 'UPDATE event_info \
            SET finish_flag = False \
            WHERE user_id =%s and id=%s;'
        values = [1, event_id]
        self.curs.execute(sql, values)
        self.connector.commit()

    def update_task_flag(self, task_id):
        sql = 'UPDATE task_info \
            SET status = 0 \
            WHERE user_id =%s and task_id=%s;'
        values = [1, task_id]
        self.curs.execute(sql, values)
        self.connector.commit()

    def update_tv_flag(self, id):
        sql = 'UPDATE watch_tv_info \
            SET status = 0 \
            WHERE user_id =%s and id=%s;'
        values = [1, id]
        self.curs.execute(sql, values)
        self.connector.commit()

    def get_health_data(self, user_id):
        sql = 'SELECT measure_date, \
                systolic_blood_pressure, diastolic_blood_pressure, \
                pulse, weight \
                FROM health_info \
                WHERE user_id =%s;'
        values = (user_id,)
        self.curs.execute(sql, values)
        return self.curs.fetchall()
    
    def get_event_view(self, user_id):
        sql = 'SELECT * FROM event_view_running \
                WHERE user_id =%s \
                ORDER BY left_days asc;'
        values = (user_id,)
        self.curs.execute(sql, values)
        return self.curs.fetchall()
    
    def get_tv_view(self, user_id):
        sql = 'SELECT * FROM tv_view_watching \
                WHERE user_id =%s \
                ORDER BY id asc;'
        values = (user_id,)
        self.curs.execute(sql, values)
        return self.curs.fetchall()
    
    def get_event_view_by_id(self, user_id, id):
        sql = 'SELECT * FROM event_view_running \
                WHERE user_id =%s AND id=%s;'
        values = (user_id, id,)
        self.curs.execute(sql, values)
        return self.curs.fetchone()
    
    def get_task_data(self, user_id):
        sql = 'SELECT * \
                FROM task_info \
                WHERE user_id =%s and status = 1 \
                ORDER BY limit_date asc;'
        values = (user_id,)
        self.curs.execute(sql, values)
        return self.curs.fetchall()
    
    def get_task_tag(self):
        sql = 'SELECT * FROM m_task_tag;'
        self.curs.execute(sql)
        return self.curs.fetchall()

    def get_task_view(self, user_id):
        sql = 'SELECT * FROM task_view_running \
                WHERE user_id =%s \
                ORDER BY left_days asc;'
        values = (user_id,)
        self.curs.execute(sql, values)
        return self.curs.fetchall()
    
    def get_task_view_by_id(self, user_id, id):
        sql = 'SELECT * FROM task_view_running \
                WHERE user_id =%s AND id=%s;'
        values = (user_id, id,)
        self.curs.execute(sql, values)
        return self.curs.fetchone()
    
    def get_tv_info_by_id(self, user_id, id):
        sql = 'SELECT * FROM watch_tv_info \
                WHERE user_id =%s AND id=%s;'
        values = (user_id, id,)
        self.curs.execute(sql, values)
        return self.curs.fetchone()
    
    def get_today_health(self, user_id):
        sql = 'SELECT * FROM view_today_health WHERE user_id =%s;'
        values = (user_id,)
        self.curs.execute(sql, values)
        return self.curs.fetchone()
    
    def get_goal_health(self, user_id):
        sql = 'SELECT * FROM view_goal_health WHERE user_id =%s;'
        values = (user_id,)
        self.curs.execute(sql, values)
        return self.curs.fetchone()
    
    def get_diff_health(self, user_id):
        sql = 'SELECT * FROM view_diff_health WHERE user_id =%s;'
        values = (user_id,)
        self.curs.execute(sql, values)
        return self.curs.fetchone()
    
    def get_today_event(self, user_id):
        sql = 'SELECT * FROM view_today_event WHERE user_id =%s;'
        values = (user_id,)
        self.curs.execute(sql, values)
        return self.curs.fetchall()
    
    def get_today_task(self, user_id):
        sql = 'SELECT * FROM view_today_task WHERE user_id =%s;'
        values = (user_id,)
        self.curs.execute(sql, values)
        return self.curs.fetchall()

    def check_date(self, data):
        sql = 'SELECT measure_date, \
                systolic_blood_pressure, diastolic_blood_pressure, \
                pulse, weight \
                FROM health_info \
                WHERE user_id =%s AND measure_date=%s;'
        values = (1,data)
        self.curs.execute(sql, values)
        if len(self.curs.fetchall()) == 0:
            return True
        else:
            return False
    
    def sharpe_data_to_graph(self, user_id):

        data_list = self.get_health_data(user_id)
        measure_dates = [d['measure_date'].strftime('%Y-%m-%d') for d in data_list]
        systolic_blood_pressures = [d['systolic_blood_pressure'] for d in data_list]
        diastolic_blood_pressures = [d['diastolic_blood_pressure'] for d in data_list]
        pulses = [d['pulse'] for d in data_list]
        weights = [float(d['weight']) for d in data_list]
        return {
            'date': measure_dates,
            'high': systolic_blood_pressures,
            'low': diastolic_blood_pressures,
            'pulse': pulses,
            'weight': weights
        }

if __name__ == '__main__':
    
    cls = SQLiteConnector()
  
