from flask import Flask, url_for
from flask_apscheduler import APScheduler
from datetime import datetime
import os

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
# @scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
def job1():
    global count
    print('Job 1 executed: ' + datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    count +=1
    s = 'count:' + str(count)
    return '/' + s


# cron examples
@scheduler.task('cron', id='do_job_2', hour='*', minute='*', second=10)
def job2():
    print('Job 2 executed' + datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    os.startfile('D:\python_pgm\music_downloader\music_data\《掌心之中》.mp3')


@app.route('/remove_job')
def delete_job():
    return 'REMOVE', 200

@app.route('/')
def index():
    os.startfile('D:\python_pgm\music_downloader\music_data\《掌心之中》.mp3')

    test_str = job1()

    return 'Hello world' + test_str

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)