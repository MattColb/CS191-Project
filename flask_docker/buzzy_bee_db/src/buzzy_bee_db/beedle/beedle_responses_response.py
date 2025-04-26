from ..db_response import DBResponse

class BeedleResponsesResponse(DBResponse):
    def __init__(self, success=None, message=None, questions=None, ):
        super().__init__(success=success, message=message)
        self.questions = questions