from flask import Blueprint, render_template, request, session, flash
import datetime
from .helper_functions.math_functions import user_response, user_response,  get_best_question

math = Blueprint('math', __name__,
                        template_folder='templates')

@math.route("/Math", methods=["GET"])
def math_page():
    if request.method == "GET":
        session.pop("current_question", None)
        return render_template("math.html")

@math.route("/MathQuestions/<qtype>", methods=["GET", "POST"])
def math_questions(qtype):
    if request.method == "GET":
        sub_account_info = session.get("sub_account_information")
        # Use the corresponding function to generate the question
        question_data = get_best_question(qtype, sub_account_info['score_in_math'])
        start_dt = datetime.datetime.utcnow().isoformat()

        # Make sure the question is set in the session before returning
        session["current_question"] = question_data
        
        return render_template("math_questions.html", question=question_data['question'], start_dt=start_dt, qtype=qtype)
    
    if request.method == "POST":
        # Handle user response (this part would remain as it is)
        return user_response(request, qtype)
