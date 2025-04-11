from buzzy_bee_db.question.question import get_question, add_question, get_closest_questions
from buzzy_bee_db.account.stu_account import update_stu_account
from flask import redirect, url_for, flash
from ..subject_class import SubjectClass
from .spelling_question_generator import SPELLING_QUESTION_TYPES, SPELLING_QUESTIONS_FUNCTIONS
import random

class SpellingFunctions(SubjectClass):
    def __init__(self, rating):
        #Should be the same across all
        qtype = random.choice(SPELLING_QUESTION_TYPES)
        super().__init__(qtype, rating)
        self.subject = "SPELLING"
        self.db_name = "score_in_spelling"

    def create_question(self):
        response = SPELLING_QUESTIONS_FUNCTIONS[self.qtype](self.rating)
        question_id = response.get("question_id")
        if get_question(question_id).success == False:
            #Add subject here
            add_question(question_id, response.get("question"), response.get("answer"), self.qtype, response.get("difficulty"), self.subject)
        return response
    
    def redirect(self):
        return redirect(url_for("spelling.spelling_page"))
    
    def get_closest_questions(self):
        return get_closest_questions(self.rating, self.qtype, self.subject)

    def update_rating(self, parent_id, student_id, new_rating):
        update_stu_account(parent_id, student_id, score_in_spelling=new_rating)

    def check_answer(self, user_answer, answer):
        #Added None because others want redirect on an error
        correct = user_answer.lower().strip() == answer.lower().strip()
        if correct:
            flash("Correct!")
        else:
            flash(f"Wrong! The correct spelling was: {answer}")
        return correct, None