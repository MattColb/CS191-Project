from ..db_response import DBResponse

class MainAccountResponse(DBResponse):
    def __init__(self, success=None, message=None, user_id=None, students=None):
        super().__init__(success=success, message=message)
        self.user_id = user_id
        self.students = students if students is not None else []