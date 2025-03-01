from ..db_response import DBResponse

class GetSubAccounts(DBResponse):
    def __init__(self, sub_accounts=None, message=None, success=None):
        super().__init__(success, message)
        self.sub_accounts = sub_accounts

class CreateSubAccount(DBResponse):
    def __init__(self, sub_account_id=None, message=None, success=None):
        super().__init__(success, message)
        self.sub_account_id = sub_account_id

class GetSubAccountResponses(DBResponse):
    def __init__(self, responses=None, message=None, success=None):
        super().__init__(success, message)
        self.responses = responses

class RecordSubAccountResponse(DBResponse):
    def __init__(self, response_id=None, message=None, success=None):
        super().__init__(success, message)
        self.response_id = response_id
