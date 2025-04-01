import random
import hashlib
import fractions
from ..generate_clock import draw_clock

# Used this chat to help with generating questions: https://chatgpt.com/share/67cc8779-7414-8013-8da8-362b5d61bb42

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

    operands = sorted(operands, reverse=True)

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
    rating = 500
    number_to_round = round(random.random() * 10000,4)
    place_values = [1, 10, 100, 1000, 10000, .01, .1, .001, .0001]
    place_value = random.choice(place_values)
    rounded_number = round(number_to_round / place_value) * place_value
    question = f"Round {number_to_round} to the nearest {place_value}"
    answer = rounded_number

    question_id = hashlib.sha256(str.encode(question)).hexdigest()

    f = {"question":question, "answer":answer, "difficulty":rating, "question_id":question_id}

    return f

def create_patterns(rating):
    """Generates a number pattern and asks for the next number."""
    start = random.randint(1, 50)  # Random starting number
    step = random.randint(0, 20)  # Common pattern steps
    length = random.randint(4, 6)  # Number of terms to display

    rating = step*25

    pattern = [start + i * step for i in range(length)]
    question = f"Complete the pattern: {', '.join(map(str, pattern[:-1]))}, ?"
    answer = pattern[-1]  # The next number in the pattern

    question_id = hashlib.sha256(str.encode(question)).hexdigest()

    f = {"question":question, "answer":answer, "difficulty":rating, "question_id":question_id}

    return f

def create_inequalities(rating):
    num1 = random.randint(1, 1000)
    num2 = random.randint(1, 1000)

    rating = 300

    question = f"Which inequality symbol makes this statement true? {num1} _ {num2}"
    answer = ">" if num1 > num2 else "<" if num1 < num2 else "="

    question_id = hashlib.sha256(str.encode(question)).hexdigest()

    f = {"question":question, "answer":answer, "difficulty":rating, "question_id":question_id}

    return f

def generate_fraction_problem(rating):
    """Generates a random fraction question covering different fraction concepts."""
    question_type = random.choice(["simplify", "compare", "add_subtract", "multiply_divide", "convert"])

    # Generate random fractions
    num1, denom1 = random.randint(1, 9), random.randint(2, 10)
    num2, denom2 = random.randint(1, 9), random.randint(2, 10)
    fraction1 = fractions.Fraction(num1, denom1)
    fraction2 = fractions.Fraction(num2, denom2)

    if question_type == "simplify":
        # Simplify a fraction
        unsimplified = fraction1.numerator * random.randint(2, 5), fraction1.denominator * random.randint(2, 5)
        question = f"Simplify the fraction: {unsimplified[0]}/{unsimplified[1]}"
        answer = str(fractions.Fraction(unsimplified[0], unsimplified[1]))

    elif question_type == "compare":
        # Compare two fractions
        question = f"Which symbol makes this true? {fraction1} _ {fraction2}"
        answer = ">" if fraction1 > fraction2 else "<" if fraction1 < fraction2 else "="

    elif question_type == "add_subtract":
        # Addition or subtraction
        operation = random.choice(["+", "-"])
        question = f"{fraction1} {operation} {fraction2} = ?"
        answer = str(fraction1 + fraction2) if operation == "+" else str(fraction1 - fraction2)

    elif question_type == "multiply_divide":
        # Multiplication or division
        operation = random.choice(["*", "÷"])
        question = f"{fraction1} {operation} {fraction2} = ?"
        answer = str(fraction1 * fraction2) if operation == "*" else str(fraction1 / fraction2)

    else:  # Convert fraction to decimal
        question = f"Convert {fraction1} to a decimal."
        answer = round(float(fraction1), 2)

    question_id = hashlib.sha256(str.encode(question)).hexdigest()

    return {"question": question, "answer": answer, "difficulty": 750, "question_id": question_id}

def generate_clock_problem(rating):
    hour = random.randint(1, 12)
    minute = random.randint(0, 11) * 5
    question = f"What time is shown on the clock?"
    answer = f"{hour}:{minute:02d}"
    question_id = hashlib.sha256(str.encode(question)).hexdigest()

    return {"question": question, "answer": answer, "difficulty": 350, "question_id": question_id}

MATH_QUESTIONS_TYPES = ["Addition", "Subtraction", "Multiplication", "Division", "Rounding", "Patterns", "Inequalities", "Fraction", "Clock"]

MATH_QUESTIONS_FUNCTIONS = {
    "Addition":create_addition,
    "Subtraction":create_subtraction,
    "Multiplication":create_multiplication,
    "Division":create_division,
    "Rounding":create_rounding,
    "Patterns":create_patterns,
    "Inequalities":create_inequalities,
    "Fraction":generate_fraction_problem,
    "Clock":generate_clock_problem
}