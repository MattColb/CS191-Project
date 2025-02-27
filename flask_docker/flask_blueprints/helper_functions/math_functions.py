import random
import hashlib
<<<<<<< HEAD
from .math_question_generator import *
from flask import flash, redirect, url_for
import datetime
from buzzy_bee_db.question.question import add_question, get_question

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
        qtype = random.choice(list(MATH_QUESTIONS_FUNCTIONS.keys()))
    response = MATH_QUESTIONS_FUNCTIONS[qtype](rating)
    create_new_question(response, qtype)
    return response


def create_new_question(response, qtype):
    question_id = response.get("question_id")
    if get_question(question_id).success == True:
        return
    #Check if question hash exists
    #If not, post it
    question_id = response.get("question_id")
    question = response.get("question")
    answer = response.get("answer")
    category = qtype
    difficulty = response.get("rating")
    add_question(question_id, question, answer, category, difficulty)
    return

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

    try:
        user_answer = float(user_answer)
    except:
        flash("Please enter a number")
        return redirect(url_for("math.math_questions", _method="GET", qtype=qtype))

    answer = get_question(question_id).question_id
    answer = answer.get("answer")

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
    # account_id = session.get("account_id")
    # sub_account_id = session.get("sub_account_id")
    pass
=======

def create_addition(rating):
    rating = 0
    operands = []
    if rating < 50:
        operands = [random.randint(0,10), random.randint(0,10)]
        rating = 10
    elif rating < 250:
        operands = [random.randint(0,1000000),random.randint(0,1000000)]
        determined_rating = ((len(operands[0]) + len(operands[1])) /14)*200
        rating = 50 + determined_rating
    #Negative
    else:
        operands = [random.randint(-1000000,1000000), random.randint(-1000000,1000000)]
        determined_rating = ((len(operands[0]) + len(operands[1])) /14)*750
        rating = 250+determined_rating
        pass
    #Multiple Operands
    #Decimals
    operands = [str(o) for o in operands]
    question = "+".join(operands)
    operands.sort()
    hash_question = "+".join(operands)
    answer = eval(question)

    question_id = hashlib.sha256(str.encode(hash_question)).hexdigest()

    f = {"operands":operands, "question":question, "answer":answer, "rating":rating, "question_id":question_id}

    return f

def create_multiplication(rating):
    # Times Tables
    rating = 0
    operands = []
    if rating < 250:
        operands = [random.randint(0,10), random.randint(0,10)]
        rating = 125
    # Larger number * Smaller Number
    elif rating < 1000:
        operands = [random.randint(0,10), random.randint(0,1000000)]
    # Larger number * larger number
    else:
        operands = [random.randint(0,1000000), random.randint(0,1000000)]
    #Decimals

    operands = [str(o) for o in operands]
    question = "*".join(operands)
    operands.sort()
    hash_question = "*".join(operands)
    answer = round(eval(question),2)

    question_id = hashlib.sha256(str.encode(hash_question)).hexdigest()

    f = {"operands":operands, "question":question, "answer":answer, "rating":rating, "question_id":question_id}

    return f

def create_subtraction(rating):
    #Bigger number is always first
    #Single digit/up to 20
    #Larger and larger numbers
    #Negative numbers
    operands = [random.randint(0,10), random.randint(0,10)]

    operands = [str(o) for o in operands]
    question = "-".join(operands)
    answer = round(eval(question),2)

    question_id = hashlib.sha256(str.encode(question)).hexdigest()

    f = {"operands":operands, "question":question, "answer":answer, "rating":rating, "question_id":question_id}

    return f

def create_division(rating):
    #Single Digit whole numbers
    # Big divided by a single digit
    # Remainders
    operands = [random.randint(0,10), random.randint(0,10)]

    operands = [str(o) for o in operands]
    question = "/".join(operands)
    answer = round(eval(question),2)

    question_id = hashlib.sha256(str.encode(question)).hexdigest()

    f = {"operands":operands, "question":question, "answer":answer, "rating":rating, "question_id":question_id}
    
    return f

def create_rounding(rating):
    #Round to 10s, 100s, thousands, etc.
    number_to_round = round(random.uniform(0,1000000),4)
    
    pass

def create_patterns(rating):
    pass


question_types = ["Addition", "Subtraction", "Multiplication", "Division", "Rounding", "Patterns", "All"]

operations = {
    "Addition":create_addition,
    "Subtraction":create_subtraction,
    "Multiplication":create_multiplication,
    "Division":create_division,
    # "Rounding":create_rounding,
    # "Patterns":create_patterns
}

def get_question(qtype, rating):
    if qtype not in question_types:
        raise Exception

    if qtype == "All":
        return random.choice(list(operations.values()))(rating)    
    return operations[qtype](rating)
>>>>>>> 4ade809 (Very sloppy first attempt at a couple of different types of questions)
