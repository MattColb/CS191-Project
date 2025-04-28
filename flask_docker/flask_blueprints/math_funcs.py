from flask import Blueprint, render_template, request, session, send_file, url_for
import datetime
from .helper_functions.question_functions import user_response,  get_best_question
from .login_register import check_sub_account_not_exists
from .helper_functions.math.generate_clock import draw_clock
from .helper_functions.math.math_functions import MathFunctions


math = Blueprint('math', __name__,
                        template_folder='templates')

@math.route("/Math", methods=["GET"])
@check_sub_account_not_exists
def math_page():
    if request.method == "GET":
        return render_template("math.html")

@math.route("/MathQuestions/<qtype>", methods=["GET", "POST"])
@check_sub_account_not_exists
def math_questions(qtype):
    if request.method == "GET":
        session.pop("current_question", None)
        sub_account_info = session.get("sub_account_information")
        math = MathFunctions(sub_account_info.get("score_in_math", 0), qtype)
        question_data = get_best_question(math)
        start_dt = datetime.datetime.utcnow().isoformat()
        
        # Make sure the question is set in the session before returning
        session["current_question"] = question_data

        new_redirect = url_for('math.math_questions', start_dt=start_dt, qtype=qtype)

        if qtype == "Clock":
            return render_template("math_questions.html", question=question_data['question'], start_dt=start_dt, qtype=qtype, time=question_data['answer'], redirect=new_redirect)

        return render_template("math_questions.html", question=question_data['question'], start_dt=start_dt, qtype=qtype, redirect=new_redirect)
    
    if request.method == "POST":
        # Handle user response (this part would remain as it is)
        sub_account_info = session.get("sub_account_information", dict())
        math = MathFunctions(sub_account_info.get("score_in_math", 0), qtype)
        return user_response(request, math)

@math.route("/Clock/<time>")
def serve_clock(time):
    img_bytes = draw_clock(time)
    return send_file(img_bytes, mimetype="image/png")