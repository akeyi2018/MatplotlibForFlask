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