import os
from dotenv import load_dotenv
import locale
from datetime import date, timedelta

load_dotenv()


class Sql_Param:
    KEY = os.getenv("S_KEY")
    host = os.getenv("host")
    user = os.getenv("user")
    passwd = os.getenv("PASSWD")
    health_database = os.getenv("health_db")
    alchemy_database = os.getenv("alchemy_db")
    debug_flag = False


class Message_list:
    finish_event = os.getenv("finish_event")
    finish_task = os.getenv("finish_task")
    finish_tv = os.getenv("finish_tv")
    user_regist_event = os.getenv("user_regist_event")


class Html_Param:

    nav_home = [
        {
            "text": "Dashboard",
            "id": "v-pills-dashboard",
            "label": "v-pills-dashboard-tab",
            "url": "dashboard.html",
            "active": True,
        },
        {
            "text": "血圧体重管理",
            "id": "v-pills-messages",
            "label": "v-pills-messages-tab",
            "url": "bodyweight_graph.html",
            "active": False,
        },
        {
            "text": "イベント一覧",
            "id": "v-pills-schedule-view",
            "label": "v-pills-schedule-view-tab",
            "url": "event.html",
            "active": False,
        },
        {
            "text": "タスク一覧",
            "id": "v-pills-task-view",
            "label": "v-pills-task-view-tab",
            "url": "task.html",
            "active": False,
        },
        {
            "text": "TVドラマ一覧",
            "id": "v-pills-tv-view",
            "label": "v-pills-tv-view-tab",
            "url": "tv.html",
            "active": False,
        },
    ]

    # nav_edu_p = [
    #     {
    #         "id": "flask_01",
    #         "text": "1. Flask"
    #     }
    # ]

    nav_edu = {
        "parent":{
             "id": "flask_01",
            "text": "1. Flask"
        },
        "nav": [
        {
            "lind_id": "index_01",
            "link_text": "FlaskとMYSQLとSQLite3について",
            "url": "sub/flask_01.html"
        },
        {
            "lind_id": "index_02",
            "link_text": "Flask-SQLAlchemy操作まとめ",
            "url": "sub/flask_02.html"
        },
        {
            "lind_id": "index_03",
            "link_text": "JavascriptとJinja2の組み合わせ",
            "url": "sub/flask_03.html"
        }]
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def mapping_data(cls, dates, data):
        # 日付をキーとしてデータをマッピング
        dict_01 = {}
        for d in dates:
            dd_01 = d.strftime("%Y-%m-%d")
            kk = d.strftime("%m月%d日（%a）")
            dict_01[kk] = []
            for item in data:
                dd2 = item[2].strftime("%Y-%m-%d")
                if dd2 in dd_01:
                    dict_01[kk].append(item)
        return dict_01

    @classmethod
    def get_home_data(cls, session):
        from db_controller import Health_info, Event_info, Task_info, Movie_info

        # 日本語で曜日の表示
        locale.setlocale(locale.LC_ALL, "")
        dt = date.today()
        view_today = dt.strftime("%Y年%m月%d日（%A）")
        view_day = [(dt + timedelta(x)) for x in range(0, 7)]

        session["id"] = 1  # 暫定的に1にする完成時は不要

        map_data = cls.mapping_data(view_day, Event_info.get_today_event())

        return {
            "dt": view_today,
            "dt2": view_day,
            "health_data": Health_info.get_record_by_user_id(session["id"]),
            "today_event": map_data,
            "today_task": Task_info.get_today_task(),
            "user": session["user_name"],
            "health_info": Health_info.get_today_health_info(),
            "running_event": Event_info.get_running_event(),
            "running_task": Task_info.get_running_task(),
            "tv_info": Movie_info.get_movie_info(session["id"]),
        }


if __name__ == "__main__":
    ins = Html_Param()
    re = ins.get_data_test()
    print(re)
