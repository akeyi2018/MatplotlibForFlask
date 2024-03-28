### 概要
Flask-SQLAlchemyを使用してデータベースに対しての基本操作のまとめ記事

### テーブル定義からテーブル作成
サンプルコードの流儀が若干違うので
```py
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'settings', 'payments_db.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    """ユーザテーブル定義
    Args:
        db (object): DB
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
@app.route('/')
def main():
    # テーブル作成
    with app.app_context():
        db.create_all()
        
    return 'Hello', 200    
```

### SELECT
```py
# クエリ
user = User.query.get(user_id)

# 複数の場合（filter)
users_to_update = User.query.filter(User.username == username_to_find, User.email == email_to_find).all()

# fetchall
# Viewに対してクエリを実行
results = MyView.query.all()

# fetchone
# Viewに対してクエリを実行して最初の結果を取得
result = MyView.query.first()

# テーブルに対して指定したカラムのみを取得してクエリを実行
results = User.query.with_entities(User.id, User.username).all()

```

### INSERT
```py
pay = Payments(user_id=2, amount=100, item='ジュース')
db.session.add(pay)
db.session.commit()

# JSON追加の場合 ->POST使用
@app.route('/add_user', methods=['POST'])
def add_user():
    # JSONデータをリクエストから取得
    data = request.get_json()

    # JSONデータからモデルのインスタンスを作成
    user = User(username=data['username'], email=data['email'])

    # モデルのインスタンスをデータベースに追加してコミット
    db.session.add(user)
    db.session.commit()

    return 'User added successfully', 201
```
### UPDATE　→PUT使用
```py
@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # 更新したいデータを取得
    user = User.query.get(user_id)
    if not user:
        return 'User not found', 404

    # リクエストデータから更新内容を取得
    data = request.json
    username = data.get('username')
    email = data.get('email')

    # 更新内容があれば、データを更新
    if username:
        user.username = username
    if email:
        user.email = email

    # データベースにコミット
    db.session.commit()

    return 'User updated successfully', 200
```

### VIEWについて
VIEWは作れないが、sqlalchemyならできる
```py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class MyView(db.Model):
    __tablename__ = 'my_view'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

# Viewを作成するSQL文
create_view_sql = """
CREATE VIEW my_view AS
SELECT id, name FROM my_table WHERE condition;
"""

# Viewを削除するSQL文
drop_view_sql = """
DROP VIEW IF EXISTS my_view;
"""

# Viewの作成
db.engine.execute(text(drop_view_sql))  # 既存のViewがあれば削除
db.engine.execute(text(create_view_sql))  # 新しいViewを作成

if __name__ == '__main__':
    app.run(debug=True)
```
物削除はなかなかしないので、割愛
