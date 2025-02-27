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
        question = get_best_question(qtype, 250)
        start_dt = datetime.datetime.utcnow().isoformat()
        return render_template("math_questions.html", question=question, start_dt=start_dt, qtype=qtype)
    if request.method == "POST":
        return user_response(request, qtype)