from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from buzzy_bee_db.question.question import get_question
from .helper_functions.math.math_functions import MathFunctions
from .helper_functions.spelling.spelling_functions import SpellingFunctions
import datetime
from .helper_functions.question_functions import user_response


beedle = Blueprint('beedle', __name__,
                        template_folder='templates')

#Left to figure out
# Choosing Questions
# Redirecting
# Checking the tracking of questions
# Getting Questions

@beedle.route("/beedle", methods=["GET", "POST"])
def run_beedle():
    if request.method == "GET":
        prev_question = session.pop("current_question", dict())
        pq = prev_question.get("question_id", None)
        
        questions = [
            "86fd799d69f0cadc0836085121279c8aec886e0e893f5e4ec651e1382b3b8ddb",
            "318684f2ba12d8825b4d69d2ad457886183c4513a238d31847f1d824f0248f46",
            "9d104a630770abd88d9f76ff4f60d032dc712fd8f3db398127a904d3aece1173"
        ]

        if pq in questions:
            pq_idx = questions.index(pq)
            questions = questions[pq_idx+1:]

        if len(questions) == 0:
            return redirect(url_for("login_register.sub_account"))

        current_question = questions[0]

        question_data = get_question(current_question).question

        qtype = question_data.get("category")

        start_dt = datetime.datetime.utcnow().isoformat()

        new_redirect = url_for("beedle.run_beedle", qtype=qtype, start_dt=start_dt)

        session["current_question"] = question_data

        if question_data.get("subject") == "MATH":
            if qtype == "Clock":
                return render_template("math_questions.html", question=question_data['question'], redirect=new_redirect,
                                       start_dt=start_dt, qtype=qtype, time=question_data['answer'])

            return render_template("math_questions.html", question=question_data['question'], redirect=new_redirect,
                                   start_dt=start_dt, qtype=qtype)

        if question_data.get("subject") == "SPELLING":
            if qtype == "Audio":
                return render_template("spelling_base.html", word=question_data["question"], start_dt=start_dt, redirect=new_redirect)
            if qtype == "Block":
                return render_template("block.html", scrambled_word = question_data["question"], start_dt=start_dt, redirect=new_redirect,
                                    word=question_data["answer"], word_length=len(question_data["question"]))

        return question_data

    if request.method == "POST":
        question_data = session.get("current_question")
        sub_account_info = session.get("sub_account_information", dict())
        qtype = question_data.get("category")
        if question_data.get("subject") == "MATH":
            math = MathFunctions(sub_account_info.get("score_in_math", 0), qtype)
            user_response(request, math)
        if question_data.get("subject") == "SPELLING":
            spelling_question = SpellingFunctions(sub_account_info.get("score_in_spelling", 0))
            user_response(request, spelling_question)
            pass
        return redirect(url_for("beedle.run_beedle"))