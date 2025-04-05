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
        user = session.get("sub_account_information")
        spelling = SpellingFunctions(user.get("spelling_rating", 0))
        question_data = get_best_question(spelling)

        start_dt = datetime.datetime.utcnow().isoformat()
        
        # Make sure the question is set in the session before returning
        session["current_question"] = question_data

        #Render the correct template
        return render_template("spelling_base.html", question=question_data['question'], start_dt=start_dt)
    
    if request.method == "POST":
        user = session.get("sub_account_information")
        spelling = SpellingFunctions(user.get("spelling_rating", 0))
        user_response(request, spelling)

@spelling.route("/Spelling/Audio/<word>", methods=["GET"])
@check_sub_account_not_exists
def spelling_audio(word):
    audio = gtts.gTTS(text=word, lang="en")

    audio_io = BytesIO()
    audio.write_to_fp(audio_io)
    audio_io.seek(0)
    return Response(audio_io, mimetype="audio/mpeg")