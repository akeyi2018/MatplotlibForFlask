import os
from dotenv import load_dotenv
load_dotenv()

class Sql_Param:
    KEY = os.getenv('S_KEY')
    host = os.getenv('host')
    user = os.getenv('user')
    passwd = os.getenv('PASSWD')
    health_database = os.getenv('health_db')

class Message_list:
    finish_event = os.getenv('finish_event')
    user_regist_event = os.getenv('user_regist_event')


class Html_Param:
    nav_home = [{
            "text": "Dashboard",
            "id": "v-pills-dashboard",
            "label": "v-pills-dashboard-tab",
            "url": "dashboard.html",
            "active": False
        },
        {
            "text": "血圧体重管理",
            "id": "v-pills-messages",
            "label": "v-pills-messages-tab",
            "url": "bodyweight_graph.html",
            "active": False
        },
        {
            "text": "タスク登録",
            "id": "v-pills-task",
            "label": "v-pills-task-tab",
            "url": "regist_task.html",
            "active": True
        },
        {
            "text": "イベント登録",
            "id": "v-pills-schedule",
            "label": "v-pills-schedule-tab",
            "url": "regist_event.html",
            "active": False
        }
    ]

    task_home = {
        "title": "タスク登録",
        "name": "タスク名：",
        "content": "詳細：",
        "limit": "期限日：",
        "category": "種類：",
        "button": "タスクを登録する"
    }
    
