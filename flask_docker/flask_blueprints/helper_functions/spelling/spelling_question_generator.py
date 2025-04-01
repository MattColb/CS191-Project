

def create_audio_question(rating):
    pass

def create_block_question(rating):
    pass

def create_image_question(rating):
    pass

SPELLING_QUESTION_TYPES = ["Audio", "Block", "Image"]
SPELLING_QUESTIONS_FUNCTIONS = {
    "Audio":create_audio_question,
    "Block":create_block_question,
    "Image":create_block_question
}