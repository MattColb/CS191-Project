from flask import Blueprint, abort, request, redirect, url_for, render_template, session, flash
import datetime
import random
from .helper_functions.math_functions import user_response, get_best_question

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
        question = get_best_question(qtype, sub_account_info.get("score_in_math"))
        start_dt = datetime.datetime.utcnow().isoformat()
        return render_template("math_questions.html", question=question, start_dt=start_dt, qtype=qtype)
    if request.method == "POST":
        user_answer = request.form.get("user_answer")
        question_id = request.args.get("question_id")
        start_dt = datetime.datetime.fromisoformat(request.args.get("start_dt"))
        answer = request.args.get("answer")

        end_dt = datetime.datetime.now()

        print((end_dt - start_dt).total_seconds())

        if user_answer == answer:
            flash("Correct")
        else:
            flash(f"Wrong, the correct answer was: {answer}")

        
        return redirect(url_for("math.math_questions", _method="GET"))
