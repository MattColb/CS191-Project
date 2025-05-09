from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from buzzy_bee_db.question.question import get_question
from .helper_functions.math.math_functions import MathFunctions
from .helper_functions.spelling.spelling_functions import SpellingFunctions
import datetime
from .helper_functions.question_functions import user_response
from buzzy_bee_db.beedle.beedle_questions import get_questions, add_questions
from buzzy_bee_db.beedle.beedle_responses import get_beedle_results, add_beedle_question_response
from .helper_functions.question_functions import get_best_question
import random

beedle = Blueprint('beedle', __name__,
                        template_folder='templates')

#
@beedle.route("/beedle", methods=["GET", "POST"])
def run_beedle():
    if request.method == "GET":
        #Get the questions
        session.pop("current_question", dict())
        pq = get_user_beedle()
        
        questions = get_beedle_questions()

        #Get the latest question they haven't answered
        if pq in questions:
            pq_idx = questions.index(pq)
            questions = questions[pq_idx+1:]

        #If they finished, exit
        if len(questions) == 0:
            return redirect(url_for("login_register.sub_account"))

        #Get the question data
        current_question = questions[0]
        question_data = get_question(current_question).question
        qtype = question_data.get("category")
        start_dt = datetime.datetime.utcnow().isoformat()
        new_redirect = url_for("beedle.run_beedle", qtype=qtype, start_dt=start_dt)
        session["current_question"] = question_data

        #If it's math, return a math question
        if question_data.get("subject") == "MATH" or qtype == "Clock":
            if qtype == "Clock":
                return render_template("math_questions.html", question=question_data['question'], redirect=new_redirect,
                                       start_dt=start_dt, qtype=qtype, time=question_data['answer'])

            return render_template("math_questions.html", question=question_data['question'], redirect=new_redirect,
                                   start_dt=start_dt, qtype=qtype)
        #If spelling, return spelling question
        if question_data.get("subject") == "SPELLING":
            if qtype == "Audio":
                return render_template("spelling_base.html", word=question_data["question"], start_dt=start_dt, redirect=new_redirect)
            if qtype == "Block":
                return render_template("block.html", scrambled_word = question_data["question"], start_dt=start_dt, redirect=new_redirect,
                                    word=question_data["answer"], word_length=len(question_data["question"]))

        return question_data

    if request.method == "POST":
        #Get the important information
        question_data = session.get("current_question")
        question_id = question_data.get("question_id")
        subaccount_id = session.get("sub_account_id")
        current_date = datetime.date.today().isoformat()
        sub_account_info = session.get("sub_account_information", dict())
        qtype = question_data.get("category")
        #If math, check the math answer
        if question_data.get("subject") == "MATH" or qtype == "Clock":
            math = MathFunctions(sub_account_info.get("score_in_math", 0), qtype)
            user_response(request, math)
            result = math.result
        #If spelling, check the spelling_question
        if question_data.get("subject") == "SPELLING":
            spelling_question = SpellingFunctions(sub_account_info.get("score_in_spelling", 0))
            user_response(request, spelling_question)
            result = spelling_question.result
            pass

        #Add the response
        add_beedle_question_response(subaccount_id, current_date, question_id, result)

        return redirect(url_for("beedle.run_beedle"))
    
#Get/Generate all beedle questions
def get_beedle_questions():
    #Get the date
    current_date = datetime.date.today().isoformat()
    db_response = get_questions(current_date)

    #If beedle doesn't exist, generate them at 0,200,400,...
    if db_response.success == False:
        question_ids = []
        for i in range(5):
            rating = i*200
            question_id = generate_question(rating)
            question_ids.append(question_id)
        add_questions(current_date, question_ids)
        db_response = get_questions(current_date)
    questions = db_response.questions
    return questions

#Get the last question that the user answered
def get_user_beedle():
    current_date = datetime.date.today().isoformat()
    subaccount_id = session.get("sub_account_id")
    responses = get_beedle_results(subaccount_id, current_date)
    latest_question_id = ""
    if len(responses.questions) != 0:
        questions = responses.questions
        latest_question_id = questions[-1].get("question_id")
    return latest_question_id

#Generate a question based on the rating chosen randomly from spelling/math
def generate_question(rating):
    question_func = random.choice([SpellingFunctions, MathFunctions])
    question_func = question_func(rating)
    question_data = get_best_question(question_func)
    question_id = question_data.get("question_id")
    return question_id