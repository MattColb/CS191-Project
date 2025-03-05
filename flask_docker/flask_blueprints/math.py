from flask import Blueprint, abort, request, redirect, url_for, render_template, session, flash
import datetime
import random
from .helper_functions.math_functions import user_response, get_best_question, user_response

math = Blueprint('math', __name__,
                        template_folder='templates')

@math.route("/Math", methods=["GET"])
def math_page():
    if request.method == "GET":
        return render_template("math.html")

@math.route("/MathQuestions/<qtype>", methods=["GET", "POST"])
def math_questions(qtype):
    if request.method == "GET":
        session["sub_account_information"] = {"sub_account_id":"9f9244fe-f5c9-4200-9afd-94372272469b",
            "sub_account_username":"Name",
            "name":"Name",
            "score_in_math":0
            }
        sub_account_info = session.get("sub_account_information")
        question = get_best_question(qtype, sub_account_info.get("score_in_math"))
        start_dt = datetime.datetime.utcnow().isoformat()
        match qtype:
            case "Addition":
                return render_template("addition.html", question=question, start_dt=start_dt, qtype=qtype)
            case _:
                return render_template("math_questions.html", question=question, start_dt=start_dt, qtype=qtype)
    if request.method == "POST":
        return user_response(request, qtype)
    
@math.route("/MathResult/<qtype>", methods=["GET"])
def math_question_result(qtype):
    if request.method == "GET":
        return render_template("math_question_result.html", qtype=qtype)