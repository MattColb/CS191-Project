from flask import Blueprint, render_template, request, session, flash
import datetime
from .helper_functions.math_functions import user_response, user_response,  get_best_question

spelling = Blueprint('spelling', __name__,
                        template_folder='templates')

@spelling.route("/Spelling", methods=["GET"])
def spelling_page():
    if request.method == "GET":
        session.pop("current_question", None)
        return "Spelling Page"

@spelling.route("/SpellingQuestion/<qtype>", methods=["GET", "POST"])
def spelling_questions(qtype):
    if request.method == "GET":
        return "Spelling Questions Page"