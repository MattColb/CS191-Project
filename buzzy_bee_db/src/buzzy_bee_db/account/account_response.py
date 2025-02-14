from buzzy_bee_db.db_response import DB_Response

class SubAccountResponse(DB_Response):
    def __init__(self, sub_user_id=None, success=None, message=None):
        super().__init__(success, message)
        self.sub_user_id = sub_user_id

    def get_sub_user_id(self):
        return self.sub_user_id

    def set_sub_user_id(self, sub_user_id):
        self.sub_user_id = sub_user_id

class SubAccountGetResponse(DB_Response):
    def __init__(self, users=None, success=None, message=None):
        super().__init__(success, message)
        self.users = users

    def get_users(self):
        return self.users

    def set_users(self, users):
        self.users = users