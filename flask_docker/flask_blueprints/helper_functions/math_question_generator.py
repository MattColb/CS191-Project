import random
import hashlib

def create_addition(rating):
    operands = []
    if rating < 50:
        operands = [random.randint(0,9), random.randint(0,9)]
        rating = 25
    elif rating < 250:
        operands = [random.randint(10, 99),random.randint(10, 99)]
        rating = 175
    #Negative
    else:
        operands = [random.randint(100,999), random.randint(100,999)]
        rating = 450
        pass
    #Multiple Operands
    #Decimals
    operands = [str(o) for o in operands]
    question = "+".join(operands)
    operands.sort()
    hash_question = "+".join(operands)
    answer = eval(question)

    question_id = hashlib.sha256(str.encode(hash_question)).hexdigest()

    f = {"question":question, "answer":answer, "difficulty":rating, "question_id":question_id}

    return f

def create_multiplication(rating):
    # Times Tables
    operands = []
    if rating < 250:
        operands = [random.randint(0,10), random.randint(0,10)]
        rating = 125
    elif rating < 550:    
        operands = [random.randint(1,10), random.randint(10,20)]
    elif rating < 1000:
        operands = [random.randint(10,99), random.randint(10,99)]
    else:
        operands = [random.randint(10,99), random.randint(10,1000)]

    operands = [str(o) for o in operands]
    question = "*".join(operands)
    operands.sort()
    hash_question = "*".join(operands)
    answer = round(eval(question),2)

    question_id = hashlib.sha256(str.encode(hash_question)).hexdigest()

    f = {"question":question, "answer":answer, "difficulty":rating, "question_id":question_id}

    return f

def create_subtraction(rating):
    #Bigger number is always first
    #Single digit/up to 20
    #Larger and larger numbers
    #Negative numbers
    operands = []
    if rating < 50:
        operands = [random.randint(0,9), random.randint(0,9)]
        rating = 10
    elif rating < 250:
        operands = [random.randint(10, 99),random.randint(10, 99)]
        rating = 125
    #Negative
    else:
        operands = [random.randint(100,999), random.randint(100,999)]
        rating = 450

    operands.sort()

    operands = [str(o) for o in operands]
    question = "-".join(operands)
    answer = eval(question)

    question_id = hashlib.sha256(str.encode(question)).hexdigest()

    f = {"question":question, "answer":answer, "difficulty":rating, "question_id":question_id}

    return f

def create_division(rating):
    if rating < 350:
        divisor = random.randint(1, 9)
        quotient = random.randint(1, 9)
        rating = 200
    elif rating < 600:
        divisor = random.randint(2, 9)
        quotient = random.randint(10, 20)
        rating = 450
    else: 
        divisor = random.randint(10, 20)
        quotient = random.randint(10, 50)
        rating = 750
    
    dividend = divisor * quotient 
    question = f"{dividend}÷{divisor}"
    answer = quotient

    question_id = hashlib.sha256(str.encode(question)).hexdigest()

    f = {"question":question, "answer":answer, "difficulty":rating, "question_id":question_id}
    
    return f

def create_rounding(rating):
    pass

def create_patterns(rating):
    pass

def create_inequalities(rating):
    pass

def create_fraction(rating):
    pass




MATH_QUESTIONS_TYPES = ["Addition", "Subtraction", "Multiplication", "Division", "Rounding", "Patterns", "Inequalities", "Fraction", "Clock"]

MATH_QUESTIONS_FUNCTIONS = {
    "Addition":create_addition,
    "Subtraction":create_subtraction,
    "Multiplication":create_multiplication,
    "Division":create_division,
    # "Rounding":create_rounding,
    # "Patterns":create_patterns,
    # "Inequalities":create_inequalities,
}