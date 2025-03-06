from flask import Blueprint, render_template, request, session, flash
import datetime
from .helper_functions.math_functions import user_response, user_response, get_best_question

math = Blueprint('math', __name__,
                        template_folder='templates')

@math.route("/Math", methods=["GET"])
def math_page():
    if request.method == "GET":
        return render_template("math.html")

@math.route("/MathQuestions/<qtype>", methods=["GET", "POST"])
def math_questions(qtype):
    if request.method == "GET":
        sub_account_info = session.get("sub_account_information")
        question_data = get_best_question(qtype, sub_account_info.get("score_in_math"))
        start_dt = datetime.datetime.utcnow().isoformat()
        
        return render_template("math_questions.html", question=question_data['question'], start_dt=start_dt, qtype=qtype)
    
    if request.method == "POST":
        # Handle user response (this part would remain as it is)
        return user_response(request, qtype)
