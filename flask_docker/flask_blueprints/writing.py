from flask import Blueprint, render_template, request, session, flash
import datetime
from .helper_functions.math_functions import user_response, user_response,  get_best_question
from .login_register import check_sub_account_not_exists

writing = Blueprint('writing', __name__,
                        template_folder='templates')

@writing.route("/Writing", methods=["GET"])
@check_sub_account_not_exists
def writing_page():
    if request.method == "GET":
        session.pop("current_question", None)
        return "Writing Page"

@writing.route("/WritingQuestion/<qtype>", methods=["GET", "POST"])
@check_sub_account_not_exists
def writing_questions(qtype):
    if request.method == "GET":
        return "Writing Questions Page"