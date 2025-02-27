import random
import hashlib

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
    pass

def create_patterns(rating):
    pass


MATH_QUESTIONS_TYPES = ["Addition", "Subtraction", "Multiplication", "Division", "Rounding", "Patterns", "All"]

MATH_QUESTIONS_FUNCTIONS = {
    "Addition":create_addition,
    "Subtraction":create_subtraction,
    "Multiplication":create_multiplication,
    "Division":create_division,
    # "Rounding":create_rounding,
    # "Patterns":create_patterns
}