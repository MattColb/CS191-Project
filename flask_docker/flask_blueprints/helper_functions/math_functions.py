import random
import hashlib
from .math_question_generator import *
from flask import flash, redirect, url_for
import datetime

# Idea: Generate Question, (Need to figure out a RL alg to decide when to create new questions and when to find closest match in database)
# Add to database if needed, 
# make person answer it, 
# use question id to get answer and compare, 
# add to person's question history (correct, time, question id)
# Adjust question and person ratings (Big question mark)

#DONE
def create_question(qtype, rating):
    """
    Take in the question type and rating, create a question, add it to the db, and return it.
    
    """
    if qtype not in MATH_QUESTIONS_TYPES:
        raise Exception

    if qtype == "All":
        response = random.choice(list(MATH_QUESTIONS_FUNCTIONS.values()))(rating)    
    response = MATH_QUESTIONS_FUNCTIONS[qtype](rating)
    add_question(response)
    return response


def add_question(question):
    #Check if question hash exists
    #If not, post it
    pass

def get_best_fit_question(subject, rating):
    # Pull questions that fit and ones that are in the user's history
    # If there are some that they missed recently, try and feed them back until they get them
    # 
    pass

def get_best_question(subject, rating):
    pass
    #Choose whether to generate or get from db
    #Get the number of questions that they have answered of that type, and the number in the questions db
    # If it's over a certain proportion, then generate a new question
    # Otherwise, try and pick out an old question
    # If they are doing really well, try generating a new question to see if they work?
    create = True
    if create:
        return create_question(subject, rating)
    else:
        return get_best_fit_question(subject, rating)

def user_response(request, qtype):
    user_answer = request.form.get("user_answer")
    question_id = request.args.get("question_id")
    start_dt = datetime.datetime.fromisoformat(request.args.get("start_dt"))
    end_dt = datetime.datetime.utcnow()

    seconds_taken = round((end_dt - start_dt).total_seconds(), 2)

    answer = get_answer(question_id)
    answer = 1
    if user_answer == answer:
        flash("Correct")
    else:
        flash(f"Wrong, the correct answer was: {answer}")

    return redirect(url_for("math.math_questions", _method="GET", qtype=qtype))

def get_answer(question_id):
    #Query things
    pass

def update_ratings(question_id, response_information):
    # If question is answered wrong, the question rating always goes up
    # If question is answered right, get the amount of time that it took them
    # (Try and keep track of summary statistics?)
    # If it took the user a much less amount of time to answer the question than they typically needed, bigger increase
    # Consider streakiness (If more people have gotten it right recently it's easier, more wrong, harder). If you've gotten more right, it's easier, etc.
    account_id = session.get("account_id")
    sub_account_id = session.get("sub_account_id")