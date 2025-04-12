import random
from flask import flash, session
import datetime
from buzzy_bee_db.question.question import get_question, update_difficulty
from buzzy_bee_db.question_user.question_user import get_question_responses, record_question_response, get_student_account_responses, get_last_20_questions
from .subject_class import SubjectClass

# Update ratings needs to change
# user response needs to change

#Adjust as needed
def get_best_question(subject_class:SubjectClass):
    rng = random.random()
    response = None
    rng=1
    if rng <= .25:
        #Try and select a question that they've missed
        previous_questions = get_student_account_responses(session.get("sub_account_id"), subject_class.subject).responses
        sorted_questions = sorted(previous_questions, key=lambda d: d["timestamp_utc"])[::-1]
        correct_set = set()
        for (i, question) in enumerate(sorted_questions):
            if i == 100:
                response = subject_class.create_question()
            if question["answered_correctly"] == True:
                correct_set.add(question["question_id"])
                continue
            if question["question_id"] in correct_set:
                continue
            question_response = get_question(question["question_id"]).question_id
            response = question_response
    elif rng <= .75:
        response = subject_class.get_closest_questions()
    if response == None:
        response = subject_class.create_question()
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


# https://chatgpt.com/share/67cc8779-7414-8013-8da8-362b5d61bb42 (Using ChatGPT to think up a little bit of a somewhat decent updating algorithm)
def update_ratings(question_id, percentile, answered_correctly, question, subject_class):
    account_id = session.get("user_id")
    sub_account_id = session.get("sub_account_id")
    sub_acct_info = session.get("sub_account_information")
    question_difficulty = question.get("difficulty")
    user_score = sub_acct_info.get(subject_class.db_name)

    #Actual calculation of rating changes
    prob_correct = 1/(1+(10**((question_difficulty-user_score)/400))) #.75
    prob_incorrect = 1 - prob_correct #.25

    #ISSUE
    #Getting the last 20 answers for the question and user for later use
    account_last_20 = get_last_20_questions(student_account_id=sub_account_id)
    question_last_20 = get_last_20_questions(question_id=question_id)


    #Making slight adjustments on a probability of correct
    new_question_difficulty_difference = (-1 * prob_incorrect if answered_correctly else 5 * prob_correct)
    new_user_difficulty_difference = (1 * prob_incorrect if answered_correctly else -5 * prob_correct)


    new_user_difficulty = new_user_difficulty_difference + user_score
    if new_user_difficulty <= 0:
        new_user_difficulty = user_score
        new_user_difficulty_difference = 0
    new_question_difficulty = new_question_difficulty_difference + question_difficulty
    if new_question_difficulty <= 0:
        new_question_difficulty = question_difficulty
        new_question_difficulty_difference = 0

    sub_account = session.get("sub_account_information")
    sub_account[subject_class.db_name] = new_user_difficulty
    session["sub_account_information"] = sub_account
    
    subject_class.update_rating(sub_account_id, new_user_difficulty)

    update_difficulty(question_id, new_question_difficulty)

    return new_user_difficulty_difference, new_question_difficulty_difference

def user_response(request, subject_class):
    user_answer = request.form.get("user_answer")
    start_dt = datetime.datetime.fromisoformat(request.args.get("start_dt"))
    end_dt = datetime.datetime.utcnow()
    question = session.get("current_question")

    # Debugging to check if current_question is available
    if question is None:
        flash("Error: No current question available.")
        print("DEBUG: current_question is not available in session.")
        return subject_class.redirect()

    seconds_taken = round((end_dt - start_dt).total_seconds(), 2)

    answer = question.get("answer")
    question_id = question.get("question_id")
    percentile = get_percentile(question_id, seconds_taken)
    
    #Redirect if it is not None since that means something went wrong
    answered_correctly, redirect = subject_class.check_answer(user_answer, answer)
    if redirect != None:
        return subject_class.redirect()

    user_rating_change, question_rating_change = update_ratings(question_id, percentile, answered_correctly, question, subject_class)

    record_question_response(session.get("sub_account_id"), question_id, seconds_taken, percentile, question_rating_change, user_rating_change, answered_correctly, subject_class.subject)

    return subject_class.redirect()