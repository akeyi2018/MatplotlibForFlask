import sqlite3

def event_info():
    conn = sqlite3.connect('./settings/health_db.db')
    # カーソルを取得
    cur = conn.cursor()
    # クエリを実行して結果を表示
    cur.execute("SELECT * FROM event_info \
                WHERE finish_flag = 1 ")
    rows = cur.fetchall()

