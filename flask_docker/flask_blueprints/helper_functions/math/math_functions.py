from .math_question_generator import MATH_QUESTIONS_FUNCTIONS, MATH_QUESTIONS_TYPES
from buzzy_bee_db.question.question import get_question, add_question
from flask import redirect, url_for
from ..subject_class import SubjectClass

class MathFunctions(SubjectClass):
    def __init__(self, qtype, rating):
        super().__init__(rating, qtype)
        self.subject = "MATH"
        self.redirect = redirect(url_for("math.math_questions", qtype=self.qtype))

    def create_question(self):
        if self.qtype not in MATH_QUESTIONS_TYPES:
            raise Exception

        response = MATH_QUESTIONS_FUNCTIONS[self.qtype](self.rating)
        question_id = response.get("question_id")
        if get_question(question_id).success == False:
            #Add subject here
            add_question(question_id, response.get("question"), response.get("answer"), self.qtype, response.get("difficulty"))
        return response
