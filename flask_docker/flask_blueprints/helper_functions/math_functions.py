import random
import hashlib
from .math_question_generator import *
from flask import flash, redirect, url_for, session
import datetime
from buzzy_bee_db.question.question import add_question, get_question, update_difficulty, get_closest_questions
from buzzy_bee_db.account.sub_account import update_sub_account
from buzzy_bee_db.question_user.question_user import get_question_responses, record_question_response, get_sub_account_responses, get_last_20_questions

#Adjust as needed
def get_best_question(subject, rating):
    #Better way to do this
    #Can't get around refreshing for an easier question
    #And if there is a good fit for a question, use it, if not, generate
    rng = random.random()
    response = None
    if rng <= .25:
        #Try and select a question that they've missed
        previous_questions = get_sub_account_responses(session.get("sub_account_id")).responses
        sorted_questions = sorted(previous_questions, key=lambda d: d["timestamp_utc"])[::-1]
        correct_set = set()
        for (i, question) in enumerate(sorted_questions):
            if i == 100:
                response = create_question(subject, rating)
            if question["answered_correctly"] == True:
                correct_set.add(question["question_id"])
                continue
            if question["question_id"] in correct_set:
                continue
            question_response = get_question(question["question_id"]).question_id
            response = question_response
    elif rng <= .75:
        response = get_closest_questions(rating, subject)
    if response == None:
        response = create_question(subject, rating)
    session["current_question"] = response
    return response


#DONE
def create_question(qtype, rating):
    if qtype not in MATH_QUESTIONS_TYPES:
        raise Exception

    response = MATH_QUESTIONS_FUNCTIONS[qtype](rating)
    question_id = response.get("question_id")
    if get_question(question_id).success == False:
        add_question(question_id, response.get("question"), response.get("answer"), qtype, response.get("difficulty"))
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


# https://chatgpt.com/share/67cc8779-7414-8013-8da8-362b5d61bb42 (Using ChatGPT to think up a little bit of a somewhat decent updating algorithm)
def update_ratings(question_id, percentile, answered_correctly, question):
    account_id = session.get("user_id")
    sub_account_id = session.get("sub_account_id")
    sub_acct_info = session.get("sub_account_information")
    question_difficulty = question.get("difficulty") 
    user_score = sub_acct_info.get("score_in_math")
    
    prob_of_correct = 1/(1+(10**((question_difficulty-user_score)/400)))

    account_last_20 = get_last_20_questions(sub_account_id=sub_account_id)
    question_last_20 = get_last_20_questions(question_id=question_id)

    #The thing that needs to change
    new_question_difficulty_difference = (-1 if answered_correctly else 5)
    new_user_difficulty_difference = (1 if answered_correctly else -5)
    new_user_difficulty = new_user_difficulty_difference + user_score
    if new_user_difficulty <= 0:
        new_user_difficulty = user_score
        new_user_difficulty_difference = 0
    new_question_difficulty = new_question_difficulty_difference + question_difficulty
    if new_question_difficulty <= 0:
        new_question_difficulty = question_difficulty
        new_question_difficulty_difference = 0


    sub_account = session.get("sub_account_information")
    sub_account["score_in_math"] = new_user_difficulty
    session["sub_account_information"] = sub_account

    update_sub_account(account_id, sub_account_id, score_in_math=new_user_difficulty)
    update_difficulty(question_id, new_question_difficulty)

    return new_user_difficulty_difference, new_question_difficulty_difference

def user_response(request, qtype):
    user_answer = request.form.get("user_answer")
    start_dt = datetime.datetime.fromisoformat(request.args.get("start_dt"))
    end_dt = datetime.datetime.utcnow()
    question = session.get("current_question")

    # Debugging to check if current_question is available
    if question is None:
        flash("Error: No current question available.")
        print("DEBUG: current_question is not available in session.")
        return redirect(url_for("math.math_questions", qtype=qtype))

    seconds_taken = round((end_dt - start_dt).total_seconds(), 2)

    try:
        user_answer = float(user_answer)
    except:
        flash("Please enter a number")
        return redirect(url_for("math.math_questions", qtype=qtype))

    answer = question.get("answer")
    question_id = question.get("question_id")

    percentile = get_percentile(question_id, seconds_taken)

    
    if user_answer == answer:
        flash("Correct")
        answered_correctly = True
    else:
        flash(f"Wrong, the correct answer was: {answer}")
        answered_correctly = False
    
    user_rating_change, question_rating_change = update_ratings(question_id, percentile, answered_correctly, question)

    record_question_response(session.get("sub_account_id"), question_id, seconds_taken, percentile, question_rating_change, user_rating_change, answered_correctly)

    # Only pop the current question after processing the answer
    session.pop("current_question")

    return redirect(url_for("math.math_questions", qtype=qtype))