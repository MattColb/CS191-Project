

def create_audio_question(rating):
    word = get_word(rating)
    question_id = "audio_" + word
    
    pass

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
    return "word"

SPELLING_QUESTION_TYPES = ["Audio", "Block", "Image"]
SPELLING_QUESTIONS_FUNCTIONS = {
    "Audio":create_audio_question,
    "Block":create_block_question,
    "Image":create_block_question
}