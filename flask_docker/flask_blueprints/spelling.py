from flask import Blueprint, render_template, request, session, flash, Response
import datetime
from .helper_functions.question_functions import user_response,  get_best_question
from .login_register import check_sub_account_not_exists
import gtts
from io import BytesIO
import random
from .helper_functions.spelling.spelling_functions import SpellingFunctions

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
        spelling_question = SpellingFunctions(sub_account_info.get("score_in_math", 0))
        question_data = get_best_question(spelling_question)
        start_dt = datetime.datetime.utcnow().isoformat()

        #Render the correct template
        if spelling_question.qtype == "Audio":
            return render_template("spelling_base.html", word=question_data["question"], start_dt=start_dt)
        if spelling_question.qtype == "Block":
            return render_template("block.html", scrambled_word = question_data["question"], start_dt=start_dt)
    
    if request.method == "POST":
        sub_account_info = session.get("sub_account_information")
        spelling_question = SpellingFunctions(sub_account_info.get("score_in_math", 0))
        return user_response(request, spelling_question)


@spelling.route("/Spelling/Audio/<word>", methods=["GET"])
@check_sub_account_not_exists
def spelling_audio(word):
    audio = gtts.gTTS(text=word, lang="en")

    audio_io = BytesIO()
    audio.write_to_fp(audio_io)
    audio_io.seek(0)
    return Response(audio_io, mimetype="audio/mpeg")