from buzzy_bee_db.question.question import get_question, add_question
from flask import redirect, url_for
from ..subject_class import SubjectClass
from .spelling_question_generator import SPELLING_QUESTION_TYPES, SPELLING_QUESTIONS_FUNCTIONS
import random

class SpellingFunctions(SubjectClass):
    def __init__(self, rating):
        #Should be the same across all
        qtype = random.choice(SPELLING_QUESTION_TYPES)
        super().__init__(rating, qtype)
        self.subject = "SPELLING"
        self.redirect = redirect(url_for("spelling.spelling_page"))

    def create_question(self):
        response = [self.qtype](self.rating)
        question_id = response.get("question_id")
        if get_question(question_id).success == False:
            #Add subject here
            add_question(question_id, response.get("question"), response.get("answer"), self.qtype, response.get("difficulty"))
        return response