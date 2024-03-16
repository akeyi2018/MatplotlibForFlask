from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import InputRequired, length
from mysql_tool import DB_Connector
from werkzeug.security import check_password_hash

class LoginForm(FlaskForm):
    username = StringField('ユーザ名：',
                            validators=[InputRequired(),
                            length(min=4, max=50)])
    password = PasswordField('パスワード：',
                            validators=[InputRequired(),
                            length(min=4,max=80)])
    remember = BooleanField('ログインしたままにする')
    def validate_password(self, password):
        # DBに接続して、user情報を取得
        ins = DB_Connector()
        user = ins.get_user_id(username=self.username.data)
    
        if user:
            if not check_password_hash(user['hash_key'], password.data):
                raise ValidationError('パスワードが違います。')
        else:
            raise ValidationError('無効なユーザ名またはパスワードです。')
        
class RegistUserForm(FlaskForm):
    username = StringField(
        'ユーザ名:',
        [InputRequired(), length(min=3, max=20)])
    mail_address = StringField(
        'Email:',
        [InputRequired(), length(min=3, max=20)])
    password = PasswordField(
        'パスワード:',
        [InputRequired(), length(min=4, max=20)])
    
    def validate_user(self, username):
        ins = DB_Connector()
        res = ins.get_user_id(self.mail_address.data)
        if res:
            raise ValidationError('すでにユーザ名が登録されています')