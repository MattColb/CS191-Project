from flask import Blueprint, render_template, request, session, flash
import datetime
from .helper_functions.math_functions import user_response, user_response,  get_best_question
from .login_register import check_sub_account_not_exists

spelling = Blueprint('spelling', __name__,
                        template_folder='templates')

@spelling.route("/Spelling", methods=["GET"])
@check_sub_account_not_exists
def spelling_page():
    if request.method == "GET":
        session.pop("current_question", None)
        return "Spelling Page"

@spelling.route("/SpellingQuestion/<qtype>", methods=["GET", "POST"])
@check_sub_account_not_exists
def spelling_questions(qtype):
    if request.method == "GET":
        return "Spelling Questions Page"