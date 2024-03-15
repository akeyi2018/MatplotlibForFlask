import flask_login

class AdminUser(flask_login.UserMixin):
    def __init__(self, user_id):
        self.id = user_id
    
    def get_id(self):
        # return AdminUser.query.get(user_id)
        return str(self.id)
    
    def is_authenticated(self):
        # ユーザーが認証されているかどうかをチェックするロジックを実装します。
        # この例では、単純化のために常に True を返します。
        return True

    def is_active(self):
        # ユーザーがアクティブであるかどうかをチェックするロジックを実装します。
        # この例では、単純化のために常に True を返します。
        return True
    
    def is_anonymous(self):
        # ユーザーが匿名であるかどうかをチェックするロジックを実装します。
        # この例では、単純化のために常に False を返します。
        return False