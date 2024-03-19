import os
from dotenv import load_dotenv
import locale
import datetime

load_dotenv()


class Sql_Param:
    KEY = os.getenv('S_KEY')
    host = os.getenv('host')
    user = os.getenv('user')
    passwd = os.getenv('PASSWD')
    health_database = os.getenv('health_db')

class Message_list:
    finish_event = os.getenv('finish_event')
    finish_task = os.getenv('finish_task')
    user_regist_event = os.getenv('user_regist_event')


class Html_Param:
    nav_home = [{
            "text": "Dashboard",
            "id": "v-pills-dashboard",
            "label": "v-pills-dashboard-tab",
            "url": "dashboard.html",
            "active": True
        },
        {
            "text": "血圧体重管理",
            "id": "v-pills-messages",
            "label": "v-pills-messages-tab",
            "url": "bodyweight_graph.html",
            "active": False
        },
        {
            "text": "イベント登録",
            "id": "v-pills-schedule",
            "label": "v-pills-schedule-tab",
            "url": "regist_event.html",
            "active": False
        },
        {
            "text": "イベント一覧表示",
            "id": "v-pills-schedule-view",
            "label": "v-pills-schedule-view-tab",
            "url": "event.html",
            "active": False
        },
        {
            "text": "タスク一覧表示",
            "id": "v-pills-task-view",
            "label": "v-pills-task-view-tab",
            "url": "task.html",
            "active": False
        }
    ]
    
    @staticmethod
    def func_home(session):
        # 自作クラス
        from mysql_tool import DB_Connector
        
        # 日本語で曜日の表示
        locale.setlocale(locale.LC_ALL, '')
        dt = datetime.date.today()
        ins = DB_Connector()
        session['id'] = 1 # 暫定的に1にする完成時は不要
        health_data = ins.sharpe_data_to_graph(session['id'])
        
        view_today = dt.strftime("%Y年%m月%d日（%A）")
        view_day = dt.strftime("%m月%d日(%a)")
        # 健康データの取得
        health_info = ins.get_today_health(session['id'])
        health_info_goal = ins.get_goal_health(session['id'])
        health_info_diff = ins.get_diff_health(session['id'])

        today_event = ins.get_today_event(session['id'])
        running_event = ins.get_event_view(session['id'])
        
        today_task = ins.get_today_task(session['id'])
        running_task = ins.get_task_view(session['id'])
        user_name = session['user_name']

        return {
            "dt" : view_today,
            "dt2" : view_day,
            "health_data" : health_data,
            "today_event" : today_event,
            "today_task" : today_task,
            "user" : user_name,
            "health_info" : health_info,
            "health_info_goal" : health_info_goal,
            "health_info_diff" : health_info_diff,
            "running_event" : running_event,
            "running_task" : running_task
        }

    @staticmethod
    def insert_task_info(request,session):
        from pytz import timezone
        from mysql_tool import DB_Connector

        session['id'] = 1 # 後で変更
        # 種類の大文字、間違いを対応
        try:
            kind = int(request.form.get('kind'))
        except:
            kind = 1

        # 種別によって、処理分かれる
        data = {
            "user_id": session['id'],
            "task_name": request.form.get('task_name'),
            "detail": request.form.get('discription'),
            "limit_date": request.form.get('entry_date'),
            "task_kind": kind,
            "status": 1,
            "regist_date": datetime.datetime.now(timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")
        }

        ins = DB_Connector()
        # 種別によって、処理分かれる
        if request.form.get('choice') == '新規':
            ins.insert_data('task_info', data)
        else:
            # 更新条件
            condition = {
                "user_id": int(session['id']),
                "task_id": int(request.form.get('task_id'))
            }
            ins.update_data('task_info', data, condition)

    @staticmethod
    def insert_health_info(request,session):
        from mysql_tool import DB_Connector
        # データを取得する
        high = request.form.get('high_bld')
        low = request.form.get('low_bld')
        pulse = request.form.get('pulse')
        weight = request.form.get('weight')
        
        userInput = request.form.get('userInput')
        
        if userInput == "True":
            # データ送信(DB登録)
            ins = DB_Connector()
            data_list = [
                datetime.date.today().strftime("%Y-%m-%d"),
                int(high),
                int(low),
                int(pulse),
                float(weight)
            ]
            ins.insert_health_data(data_list)
            return True, high, low, pulse, weight
        else:
            return False, high, low, pulse, weight

           
        






