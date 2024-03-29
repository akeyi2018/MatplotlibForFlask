from form_list import (
    LoginForm,
    RegistUserForm,
    RegistTaskForm,
    RegistEventForm,
    RegistTVForm,
    RegistHealthForm,
)

from db_controller import (
    User_info,
    m_Countries,
    m_genre,
    m_task_tag,
    Health_info,
    Event_info,
    Task_info,
    Movie_info,
)

# イベントフォーム設定
def set_event_form(id, session):
    id = int(id)
    if id == 0:
        form = RegistEventForm()
    else:
        # idがゼロでない場合は、既存の情報を取得する
        event_info = Event_info.get_event_by_id(int(session["id"]), id)
        if event_info:
            form = RegistEventForm(
                event_id=id,
                event_name=event_info.event_name,
                discription=event_info.discription,
                entry_date=event_info.event_date,
                kind=99,
                choice="更新",
            )
    return form

def set_task_form(id,session):
    id = int(id)
    if id == 0:  # 新規登録
        form = RegistTaskForm(task_id=id)
        form.kind.choices = [(item.id, item.tag) for item in m_task_tag.query.all()]
    else:  # 編集 既存の情報を取得する
        task_info = Task_info.get_task_by_id(int(session["id"]), id)
        if task_info:
            form = RegistTaskForm(
                task_id=id,
                task_name=task_info.task_name,
                discription=task_info.discription,
                entry_date=task_info.limit_date,
                kind=task_info.task_kind,
                choice="更新",
            )
            form.kind.choices = [(item.id, item.tag) for item in m_task_tag.query.all()]
    return form 

def set_tv_form(id,session):
    id = int(id)
    if id == 0:
        form = RegistTVForm()
        # ジャンルと製作国のカテゴリをロードする
        form.genre.choices = [(item.id, item.genre) for item in m_genre.query.all()]
        form.country.choices = [
            (item.id, item.name) for item in m_Countries.query.all()
        ]
    else:
        movie_info = Movie_info.query.filter(Movie_info.id == id).first()
        if movie_info:
            form = RegistTVForm(
                id=movie_info.id,
                title=movie_info.title,
                episodes=movie_info.episodes,
                watched=movie_info.watched,
                pub_date=movie_info.pub_date,
                genre=movie_info.genre,
                country=movie_info.country,
                discription=movie_info.discription,
                tag=movie_info.tag,
                point=movie_info.rating,
            )
            form.genre.choices = [(item.id, item.genre) for item in m_genre.query.all()]
            form.country.choices = [
                (item.id, item.name) for item in m_Countries.query.all()
            ]
    return form
