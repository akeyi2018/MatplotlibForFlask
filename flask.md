### 背景
筆者はFlaskを構築しているが、従来のMySQLを使っていました。
Flask-SQLAlchemyについては、ほとんど触れずにいました。
そこで気軽にデータベースとして使えるSQLiteとMySQLとFlaskとのやりとりの中で、なにか一番ベストな選択かについて考察しました。

### 結論
1. 拘りがなく、お試しで使いたい場合→「Flask-SQLAlchemy」
1. 持ち出ししたい、IoTなどセンサーのデータを扱う場合→SQLite
1. 本格的開発したい→MySQL

### Flask-SQLAlchemyについて
Flask-SQLAlchemyはFlaskと外部DBとの統合しやすく作られているので、筆者は、これから使ってみたいと思う。
また、従来の使い方とFlask流の使い方について理解したら、どこかで記事を書きたいと思う。

### 基本的な使い方
以下は基本的な使い方をおさらいする

## SQLite(Flask)

以下のように完全にPythonでDBにデータを入れているので、SQL文を使わずにできそう。

```py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

with app.app_context():
    db.create_all()
    
user = User(username='john', email='john@example.com')
db.session.add(user)
db.session.commit()
```
MYSQLを使う場合
```py
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

    def create_table(self):
        sql = """CREATE TABLE user_info
            (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `name` VARCHAR(100) DEFAULT NULL,
                `mail_address` VARCHAR(255) DEFAULT NULL,
                `hash_key` TEXT
            ); """
        self.curs.execute(sql)
        
    def insert_user(self, data):
        sql = "INSERT INTO user_info (name, mail_address, hash_key) VALUES \
            (%s, %s, %s)"
        self.curs.execute(sql, data)
        self.connector.commit()

# データ登録
data = ['john', 'john@example.com','HASH_KEY']
ins = DB_Connector()
ins.create_table()
ins.insert_user(data)
```
ちょっとソースの量が増えるので、また、バグなどがあった場合どうしても、行ったり来たりするので、
筆者は頑張って、Flask-SQLAlchemyを使っていこうかと考えています。

MYSQLとFlaskを統合したFlask-SQLAlchemyについて以下のように使います
```py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@hostname/db_name'
db = SQLAlchemy(app)

# 以後はSQLiteと同じ
```

