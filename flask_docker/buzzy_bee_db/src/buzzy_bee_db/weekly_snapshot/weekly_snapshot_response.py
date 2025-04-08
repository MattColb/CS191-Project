from ..db_response import DBResponse

class WeeklySnapshotResponse(DBResponse):
    def __init__(self, success=None, message=None, response_id=None, response=None, responses=None):
        super().__init__(success=success, message=message)
        self.response_id = response_id 
        self.response = response 
        self.responses = responses
