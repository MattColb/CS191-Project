from flask import Blueprint, render_template, request, session, flash, Response
import datetime
from .helper_functions.math_functions import user_response, user_response,  get_best_question
from .login_register import check_sub_account_not_exists
import gtts
from io import BytesIO
import random

spelling = Blueprint('spelling', __name__,
                        template_folder='templates')

@spelling.route("/Spelling", methods=["GET", "POST"])
@check_sub_account_not_exists
def spelling_page():
    if request.method == "GET":
        # List of potential words:
        words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"]
        current_word = random.choice(words)
        
        #Remove previous question
        session.pop("current_question", None)

        #Get spelling question


        #Render the correct template
        return render_template("spelling_base.html", word=current_word)
    
    if request.method == "POST":
        # Get the user's answer
        user_answer = request.form.get("user_answer")
        current_word = session.get("current_question")

        # Check if the answer is correct
        if user_answer.lower() == current_word.lower():
            flash("Correct!")
        else:
            flash(f"Incorrect! The correct spelling is {current_word}.")


@spelling.route("/Spelling/Audio/<word>", methods=["GET"])
@check_sub_account_not_exists
def spelling_audio(word):
    audio = gtts.gTTS(text=word, lang="en")

    audio_io = BytesIO()
    audio.write_to_fp(audio_io)
    audio_io.seek(0)
    return Response(audio_io, mimetype="audio/mpeg")