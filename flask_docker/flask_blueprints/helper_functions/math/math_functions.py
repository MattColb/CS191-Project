from .math_question_generator import MATH_QUESTIONS_FUNCTIONS, MATH_QUESTIONS_TYPES
from buzzy_bee_db.question.question import get_question, add_question, get_closest_questions
from buzzy_bee_db.account.stu_account import update_stu_account
from flask import redirect, url_for, flash
from ..subject_class import SubjectClass
import numbers

class MathFunctions(SubjectClass):
    def __init__(self, qtype, rating):
        super().__init__(rating, qtype)
        self.subject = "MATH"
        self.db_name = "score_in_math"

    def create_question(self):
        if self.qtype not in MATH_QUESTIONS_TYPES:
            raise Exception

        response = MATH_QUESTIONS_FUNCTIONS[self.qtype](self.rating)
        question_id = response.get("question_id")
        if get_question(question_id).success == False:
            #Add subject here
            add_question(question_id, response.get("question"), response.get("answer"), self.qtype, response.get("difficulty"), self.subject)
        return response

    def get_closest_questions(self):
        return get_closest_questions(self.rating, self.qtype, self.subject)
    
    def check_answer(self, user_answer, answer):
        #This will be different
        if isinstance(answer, numbers.Number):
            answer = round(answer, 2)
            try:
                user_answer = round(float(user_answer), 2)
            except ValueError:
                flash("Invalid answer format. Please enter a number.")
                return None, "Error"
        if user_answer == answer:
            flash("Correct")
            answered_correctly = True
        else:
            flash(f"Wrong, the correct answer was: {answer}")
            answered_correctly = False

        return answered_correctly, None
    
    def update_rating(self, student_id, new_rating):
        update_stu_account(student_id, score_in_math=new_rating)

    def redirect(self):
        return redirect(url_for("math.math_questions", qtype=self.qtype))