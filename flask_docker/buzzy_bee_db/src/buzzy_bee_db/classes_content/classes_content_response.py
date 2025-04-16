from ..db_response import DBResponse

class ClassContentResponse(DBResponse):
    def __init__(self, success=None, message=None, class_id=None, class_information=None, content_id=None, content_information=None):
        super().__init__(success=success, message=message)
        self.class_id = class_id
        self.class_information = class_information
        self.content_id = content_id
        self.content_information = content_information
