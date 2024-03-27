import os
from settings import Sql_Param

def initialize_app(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        os.getcwd(), "settings", "health_db.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
   
    app.config["SECRET_KEY"] = Sql_Param.KEY

    # db_uri = f'mysql+pymysql://{Sql_Param.user}:{Sql_Param.passwd}@{Sql_Param.host}/{Sql_Param.alchemy_database}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    return app
