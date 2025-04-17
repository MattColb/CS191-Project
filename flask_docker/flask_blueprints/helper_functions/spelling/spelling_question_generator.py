#Questions need: question, answer, question id, difficulty
import hashlib
import random
from wonderwords import RandomWord
import random

def create_audio_question(rating):
    print(type(rating))
    current_word, rating = get_word(rating)

    question_id = hashlib.sha256(str.encode("audio_"+current_word)).hexdigest()

    return {"question":current_word, "answer":current_word, "difficulty":rating, "question_id":question_id}

def create_block_question(rating):
    current_word, rating = get_word(rating)
    question_id = "block_" + current_word

    word_list = list(current_word)

    random.shuffle(word_list)
    
    question_id = hashlib.sha256(str.encode("audio_"+current_word)).hexdigest()

    return {"question":"".join(word_list), "answer":current_word, "difficulty":rating, "question_id":question_id}

def get_word(rating):
    length = int((rating//100)+1)
    r = RandomWord()
    word = r.word(word_max_length=length+2, word_min_length=length)
    return word, (length-1)*100

SPELLING_QUESTION_TYPES = ["Block", "Audio"]
SPELLING_QUESTIONS_FUNCTIONS = {
    "Audio":create_audio_question,
    "Block":create_block_question,
}