from ..db_response import DBResponse

class TeacherAccountResponse(DBResponse):
    def __init__(self, success=None, message=None, teacher_id=None, students=None):
        super().__init__(success=success, message=message)
        self.teacher_id = teacher_id
        self.students = students if students is not None else []
