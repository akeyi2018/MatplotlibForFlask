from datetime import datetime
import mysql.connector as myconnector
from settings import Sql_Param
from werkzeug.security import generate_password_hash
from pytz import timezone

class DB_Connector:
    def __init__(self) -> None:
        try:
            self.connector = myconnector.connect(
                host=Sql_Param.host,
                user=Sql_Param.user,
                password=Sql_Param.passwd,
                database=Sql_Param.health_database
            )
            self.curs = self.connector.cursor(dictionary=True,buffered=True)
        except Exception as e:
            print(f'Error Occurred: {e}')
    
    def insert_public_user(self):
        sql = "INSERT INTO user_info (regist_time, name, mail_address, hash_key) VALUES \
            (%s, %s, %s, %s)"
        values = [
            datetime.now(timezone('Asia/Tokyo')),
            'Akeyi',
            'akeyi2016@gmail.com',
            generate_password_hash('testtest', salt_length=8)
        ]
        self.curs.execute(sql, values)
        self.connector.commit()

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
    
    def insert_event_data(self, data):
        sql = "INSERT INTO event_info \
                (user_id, event_name, event_date, \
                discription, finish_flag, \
                create_time) VALUES \
                (%s, %s, %s, %s, %s, %s) "
        value1= [1]
        value2 = [True, datetime.now(timezone('Asia/Tokyo'))]
        values = value1 + data + value2
        self.curs.execute(sql, values)
        self.connector.commit()

    def update_event_flag(self, event_id):
        sql = 'UPDATE event_info \
            SET finish_flag = False \
            WHERE user_id =%s and id=%s;'
        values = [1, event_id]
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

    def get_event_data(self, user_id):
        sql = 'SELECT id, event_name, \
                event_date, discription \
                FROM event_info \
                WHERE user_id =%s and finish_flag = True \
                ORDER BY event_date asc;'
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
    
    cls = DB_Connector()
    # cls.check_date()
    data = ['横浜現場訪問','2024-03-14','交通費請請求するのを忘れずに']
    # cls.insert_event_data(data)
    # re = cls.get_event_data(1)
    # print(re)
    cls.update_event_flag(7)


    # cls.insert_public_user()
    # data = ['2024-03-13', 140, 100, 70, 76.8]

    # cls2 = MatGrapics()
    # data = cls2.get_json_data()
    # print(data)
    # for dt, high, low, pl, wt in zip(data['date'], data['high'], data['low'], data['pulse'], data['weight']):
    #     cls.insert_health_data([dt,high,low,pl,wt])

    # cls.insert_health_data(data)
    # data_list = cls.get_health_data(1)
    
    # measure_dates = [d['measure_date'].strftime('%Y-%m-%d') for d in data_list]
    # systolic_blood_pressures = [d['systolic_blood_pressure'] for d in data_list]
    # diastolic_blood_pressures = [d['diastolic_blood_pressure'] for d in data_list]
    # pulses = [d['pulse'] for d in data_list]
    # weights = [float(d['weight']) for d in data_list]

    # print(measure_dates, weights, systolic_blood_pressures)


  

   