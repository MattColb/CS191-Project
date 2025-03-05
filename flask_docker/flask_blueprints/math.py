from flask import Blueprint, render_template, request, session, flash
import datetime
from .helper_functions.math_question_generator import MATH_QUESTIONS_FUNCTIONS
from .helper_functions.math_functions import user_response, user_response

math = Blueprint('math', __name__,
                        template_folder='templates')

@math.route("/Math", methods=["GET"])
def math_page():
    if request.method == "GET":
        return render_template("math.html")

@math.route("/MathQuestions/<qtype>", methods=["GET", "POST"])
def math_questions(qtype):
    if request.method == "GET":
        session["sub_account_information"] = {
            "sub_account_id": "9f9244fe-f5c9-4200-9afd-94372272469b",
            "sub_account_username": "Name",
            "name": "Name",
            "score_in_math": 0
        }
        sub_account_info = session.get("sub_account_information")
        # Use the corresponding function to generate the question
        question_data = MATH_QUESTIONS_FUNCTIONS[qtype](sub_account_info.get("score_in_math"))
        start_dt = datetime.datetime.utcnow().isoformat()

        # Make sure the question is set in the session before returning
        session["current_question"] = question_data
        
        return render_template("math_questions.html", question=question_data['question'], start_dt=start_dt, qtype=qtype)
    
    if request.method == "POST":
        # Handle user response (this part would remain as it is)
        return user_response(request, qtype)
