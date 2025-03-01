import random
import hashlib
from .math_question_generator import *
from flask import flash, redirect, url_for, session
import datetime
from buzzy_bee_db.question.question import add_question, get_question, update_difficulty
from buzzy_bee_db.account.sub_account import update_sub_account
from buzzy_bee_db.question_user.question_user import get_question_responses, record_question_response

# Idea: Generate Question, (Need to figure out a RL alg to decide when to create new questions and when to find closest match in database)
# Add to database if needed, 
# make person answer it, 
# use question id to get answer and compare, 
# add to person's question history (correct, time, question id)
# Adjust question and person ratings (Big question mark)


def get_best_fit_question(subject, rating):
    # Pull questions that fit and ones that are in the user's history
    # If there are some that they missed recently, try and feed them back until they get them
    # 
    return False, dict()

def update_ratings():
    # If question is answered wrong, the question rating always goes up
    # If question is answered right, get the amount of time that it took them
    # (Try and keep track of summary statistics?)
    # If it took the user a much less amount of time to answer the question than they typically needed, bigger increase
    # Consider streakiness (If more people have gotten it right recently it's easier, more wrong, harder). If you've gotten more right, it's easier, etc.
    account_id = session.get("account_id")
    sub_account_id = session.get("sub_account_id")

    new_user_difficulty = 0
    # update_sub_account(account_id, sub_account_id, score_in_math=new_user_difficulty)

    new_question_difficulty = 0
    # update_difficulty(question_id, new_question_difficulty)
    pass
    return new_user_difficulty, new_question_difficulty

def get_best_question(subject, rating):
    #Better way to do this
    #Can't get around refreshing for an easier question
    #And if there is a good fit for a question, use it, if not, generate
    if session.get("current_question") != None:
        response = session.get("current_question")
        return response
    success, response = get_best_fit_question(subject, rating)
    if not success:
        return create_question(subject, rating)
    return response 

#DONE
def create_question(qtype, rating):
    if qtype not in MATH_QUESTIONS_TYPES:
        raise Exception

    if qtype == "All":
        qtype = random.choice(list(MATH_QUESTIONS_FUNCTIONS.keys()))
    response = MATH_QUESTIONS_FUNCTIONS[qtype](rating)
    question_id = response.get("question_id")
    if get_question(question_id).success == False:
        add_question(question_id, response.get("question"), response.get("answer"), qtype, response.get("rating"))
    session["current_question"] = response
    return response


def get_percentile(question_id, user_time):
    response = get_question_responses(question_id)
    question_responses = response.responses
    time_taken = [q["time_taken"] for q in question_responses]
    if len(time_taken) == 0:
        return 100
    time_taken.sort()
    count = sum(1 for x in time_taken if x <= user_time)
    percentile = round((count/ len(time_taken))*100, 2)
    return percentile

def user_response(request, qtype):
    user_answer = request.form.get("user_answer")
    start_dt = datetime.datetime.fromisoformat(request.args.get("start_dt"))
    end_dt = datetime.datetime.utcnow()
    response = session.get("current_question")

    seconds_taken = round((end_dt - start_dt).total_seconds(), 2)

    try:
        user_answer = float(user_answer)
    except:
        flash("Please enter a number")
        return redirect(url_for("math.math_questions", _method="GET", qtype=qtype))

    answer = response.get("answer")
    question_id = response.get("question_id")

    percentile = get_percentile(question_id, seconds_taken)
    
    if user_answer == answer:
        flash("Correct")
        answered_correctly = True
    else:
        flash(f"Wrong, the correct answer was: {answer}")
        answered_correctly = False
    
    user_rating_change, question_rating_change = update_ratings()

    record_question_response(session.get("sub_account_id"), question_id, seconds_taken, percentile, question_rating_change, user_rating_change, answered_correctly)

    session.pop("current_question")

    return redirect(url_for("math.math_questions", _method="GET", qtype=qtype))