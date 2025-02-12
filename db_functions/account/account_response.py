from db_functions.db_response import DB_Response

class AccountResponse(DB_Response):
    def __init__(self, success=None, message=None, user_id=None):
        super().__init__(success, message)
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

class SubAccountResponse(DB_Response):
    def __init__(self, success=None, message=None, user_id=None):
        super().__init__(success, message)
        