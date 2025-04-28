from flask import Blueprint, render_template, request, session, flash, Response, url_for
import datetime
from .helper_functions.question_functions import user_response, get_best_question
from .login_register import check_sub_account_not_exists
import gtts
from io import BytesIO
from .helper_functions.spelling.spelling_functions import SpellingFunctions
from dotenv import load_dotenv
import os
import requests

spelling = Blueprint('spelling', __name__,
                        template_folder='templates')

@spelling.route("/Spelling", methods=["GET", "POST"])
@check_sub_account_not_exists
def spelling_page():
    if request.method == "GET":
        #Remove previous question
        session.pop("current_question", None)

        #Get spelling question
        sub_account_info = session.get("sub_account_information")
        spelling_question = SpellingFunctions(sub_account_info.get("score_in_spelling", 0))
        question_data = get_best_question(spelling_question)
        start_dt = datetime.datetime.utcnow().isoformat()


        new_redirect = url_for('spelling.spelling_page', start_dt=start_dt)

        #Render the correct template
        if spelling_question.qtype == "Audio":
            return render_template("spelling_base.html", word=question_data["question"], start_dt=start_dt, redirect=new_redirect)
        if spelling_question.qtype == "Block":
            return render_template("block.html", scrambled_word = question_data["question"], start_dt=start_dt, 
                                   word=question_data["answer"], word_length=len(question_data["question"]), redirect=new_redirect)
    
    if request.method == "POST":
        sub_account_info = session.get("sub_account_information", dict())
        spelling_question = SpellingFunctions(sub_account_info.get("score_in_spelling", 0))
        return user_response(request, spelling_question)


@spelling.route("/Spelling/Audio/<word>", methods=["GET"])
@check_sub_account_not_exists
def spelling_audio(word):
    sentence = get_example(word)
    audio = gtts.gTTS(text=sentence, lang="en")

    audio_io = BytesIO()
    audio.write_to_fp(audio_io)
    audio_io.seek(0)
    return Response(audio_io, mimetype="audio/mpeg")

def get_example(word):
    load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../.env"))
    api_key = os.getenv("SPELLING_API_KEY")
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/examples"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com"
    }

    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        examples = r.json().get("examples", [])
        if len(examples) != 0:
            sentence = examples[0]
            sentence = word + ". " + word + ". " + sentence
            return sentence
    return "Your word is " + word