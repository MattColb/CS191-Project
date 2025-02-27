from ..db_response import DBResponse

class QuestionResponse(DBResponse):
    def __init__(self, success=None, message=None, question_id=None):
        super().__init__(success=success, message=message)
        self.question_id = question_id