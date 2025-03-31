from ..db_response import DBResponse

class GetStuAccounts(DBResponse):
    def __init__(self, stu_accounts=None, message=None, success=None):
        super().__init__(success, message)
        self.stu_accounts = stu_accounts

class CreateStuAccount(DBResponse):
    def __init__(self, student_id=None, message=None, success=None):
        super().__init__(success, message)
        self.student_id = student_id

class GetStuAccountResponses(DBResponse):
    def __init__(self, responses=None, message=None, success=None):
        super().__init__(success, message)
        self.responses = responses

class RecordStuAccountResponse(DBResponse):
    def __init__(self, response_id=None, message=None, success=None):
        super().__init__(success, message)
        self.response_id = response_id

class GetStuAccount(DBResponse):
    def __init__(self, stu_account=None, message=None, success=None):
        super().__init__(success, message)
        self.stu_account = stu_account
