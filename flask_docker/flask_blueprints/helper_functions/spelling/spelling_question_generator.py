#Questions need: question, answer, question id, difficulty
import hashlib
import random

def create_audio_question(rating):
    words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"]
    current_word = random.choice(words)

    question_id = hashlib.sha256(str.encode("audio"+current_word)).hexdigest()

    return {"question":current_word, "answer":current_word, "difficulty":100, "question_id":question_id}

def create_block_question(rating):
    word = get_word(rating)
    question_id = "block_" + word
    
    pass

def create_image_question(rating):
    word = get_word(rating)
    question_id = "image_" + word

    pass

def get_word(rating):
    pass


# TODO:
# , "Block", "Image"
SPELLING_QUESTION_TYPES = ["Audio"]
SPELLING_QUESTIONS_FUNCTIONS = {
    "Audio":create_audio_question,
    "Block":create_block_question,
    "Image":create_block_question
}