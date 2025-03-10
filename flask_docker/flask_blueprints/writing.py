from flask import Blueprint, render_template, request, session, flash
import datetime
from .helper_functions.math_functions import user_response, user_response,  get_best_question

writing = Blueprint('writing', __name__,
                        template_folder='templates')

@writing.route("/Writing", methods=["GET"])
def writing_page():
    if request.method == "GET":
        session.pop("current_question", None)
        return "Writing Page"

@writing.route("/WritingQuestion/<qtype>", methods=["GET", "POST"])
def writing_questions(qtype):
    if request.method == "GET":
        return "Writing Questions Page"