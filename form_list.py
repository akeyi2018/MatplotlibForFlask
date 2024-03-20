from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField, 
    BooleanField, 
    ValidationError, 
    DateField,
    SubmitField,
    SelectField,
    HiddenField,
    IntegerField,
    )
from wtforms.validators import InputRequired, length
from mysql_tool import DB_Connector
from werkzeug.security import check_password_hash
from wtforms.widgets import TextArea

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
        

class RegistTaskForm(FlaskForm):
    task_id = HiddenField('ID:')
    style1={'style': 'margin-top:1em;margin-right:300px;'}
    task_name = StringField('タスク名：',
        [InputRequired(), length(min=3, max=30)], render_kw=style1)
    style2={'style': 'margin-top:1em;margin-right:335px;'}
    entry_date = DateField('日付：', format = '%Y-%m-%d', render_kw=style2)
    style3={'style': 'width:85%; margin-top:1em;margin-right:-12px;'}
    discription = StringField('詳細：',
        [InputRequired(), length(min=3, max=50)], render_kw=style3)
    style4={'style': 'width:10%; margin-top:1em;margin-right:415px;'}
    kind = StringField('種類：',
        [InputRequired(), length(min=1, max=3)], render_kw=style4)
    choice = SelectField('種別：', choices=["新規","更新"], render_kw=style4)
    style5={'style': 'margin-top:1em;'}
    submit = SubmitField('タスクを登録する', render_kw=style5)

class RegistEventForm(FlaskForm):
    event_id = HiddenField('ID:')
    style1={'style': 'margin-top:1em;margin-right:300px;'}
    event_name = StringField('イベント名：',
        [InputRequired(), length(min=3, max=30)], render_kw=style1)
    style2={'style': 'margin-top:1em;margin-right:335px;'}
    entry_date = DateField('日付：', format = '%Y-%m-%d', render_kw=style2)
    style3={'style': 'width:85%; margin-top:1em;margin-right:-12px;'}
    discription = StringField('内容：',
        [InputRequired(), length(min=3, max=50)], render_kw=style3)
    style4={'style': 'width:10%; margin-top:1em;margin-right:415px;'}
    
    choice = SelectField('種別：', choices=["新規","更新"], render_kw=style4)
    style5={'style': 'margin-top:1em;'}
    submit = SubmitField('イベントを登録する', render_kw=style5)

class RegistTVForm(FlaskForm):
    id = HiddenField('ID:')
    style1={'style': 'width:50%;margin-top:1em;margin-right:150px;'}
    title = StringField('タイトル：',
        [InputRequired(), length(min=3, max=50)], render_kw=style1)
    style_int={'style': 'width:60px;margin-right:380px;margin-top:1em;'}
    episodes = IntegerField('回数：', [InputRequired()], default=1, render_kw=style_int)
    watched = IntegerField('鑑賞：', default=0, render_kw=style_int)
    style2={'style': 'margin-top:1em;margin-right:320px;'}
    pub_date = DateField('日付：', format = '%Y-%m-%d', render_kw=style2)

    style_choice={'style': 'width:120px;margin-right:310px;margin-top:1em;'}
    genre_list =  [(1, "アニメ"),(2, "海外ドラマ"),(3, "SFドラマ"),(4,"サスペンス"),(5,"映画")]
    genre = SelectField('ジャンル：', choices=genre_list, render_kw=style_choice)
    tag = IntegerField('tag：',default=1, render_kw=style_int)

    countries = [(1, "日本"),(2, "アメリカ"),(3, "中国"),(4,"そのた")]
    country = SelectField('製作国：', choices=countries, render_kw=style_choice)
    
    style3={'style': 'width:85%; margin-top:1em;margin-right:-12px;'}
    
    # discription = StringField('内容：',
    #     [InputRequired(), length(min=3, max=1000)], widget=TextArea, render_kw=style3)
    discription = StringField('内容：',
        widget=TextArea(), render_kw=style3)
    rating = [(1, "★"),(2, "★★"),(3, "★★★"),(4,"★★★★"), (5,"★★★★★")]
    point = SelectField('評価点：', choices=rating, default=3, render_kw=style_choice)

    style4={'style': 'width:15%; margin-top:1em;margin-right:360px;'}
    choice = SelectField('種別：', choices=[(0,"新規"),(1,"更新")], render_kw=style4)
    style5={'style': 'margin-top:1em;'}
    submit = SubmitField('登録する', render_kw=style5)

    