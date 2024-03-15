from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, length


class LoginForm(FlaskForm):
    username = StringField('ユーザ名：', validators=[InputRequired(), length(min=4, max=50)])
    password = PasswordField('パスワード：', validators=[InputRequired(), length(min=8,max=80)])
    remember = BooleanField('ログインしたままにする')
    # def validate_password(self, password):
    #     cls = User()
    #     user = cls.get_user(user_name=self.username.data)
    #     if user:
    #         if not check_password_hash(user['hash_key'], password.data):
    #             raise ValidationError('パスワードが違います。')
    #     else:
    #         raise ValidationError('無効なユーザ名またはパスワードです。')