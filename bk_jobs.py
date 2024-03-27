from flask import Flask, url_for
from flask_apscheduler import APScheduler
from datetime import datetime

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

# create app
app = Flask(__name__)
app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

count = 0

# interval example
@scheduler.task('interval', id='do_job_1', seconds=10, misfire_grace_time=900)
def job1():
    global count
    print('Job 1 executed: ' + datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    count +=1
    s = 'count:' + str(count)
    # index関数に渡すためにURLを生成
    return '/' + s

@app.route('/')
def index():
    # job1関数から渡されたURLを受け取り、その内容を表示
    test_str = job1()
    return 'Hello world ' + test_str

if __name__ == '__main__':
    app.run(debug=True)
