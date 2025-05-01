from flask import Blueprint, abort, request, redirect, url_for, render_template, session
from jinja2 import TemplateNotFound
from .helper_functions.login_register import LoginRegisterHandler
from buzzy_bee_db.account.stu_account import get_stu_accounts_main, get_stu_account, get_stu_accounts_teacher
from functools import wraps
from buzzy_bee_db.classes_content.classes_content import get_teacher_classes
from buzzy_bee_db.beedle.beedle_responses import get_beedle_results
import datetime

login_register = Blueprint('login_register', __name__,
                        template_folder='templates')


# If user trying to access something that needs user when they are not
#redirect them to login
def check_user_id_not_exists(func):
    @wraps(func)
    def check_id_exists(*kwargs, **args):
        if session.get("user_id") == None:
            return redirect("/Login")
        return func(*kwargs, **args)
        
    return check_id_exists

#If user is verified with a user id:
#restrict them from accessing the resource
def check_user_id_exists(func):
    @wraps(func)
    def check_user_id_dne(*kwargs, **args):
        if session.get("user_id") != None:
            if session.get("user_type") == "teacher":
                return redirect("/Teacher")
            return redirect("/Account")
        return func(*kwargs, **args)
    return check_user_id_dne

#If user is verified with a user id:
#But is not verified with a student id, restrict them from accessing
def check_sub_account_not_exists(func):
    @wraps(func)
    def check_sub_exists(*kwargs, **args):
        if session.get("sub_account_id") == None:
            if session.get("user_type") == "teacher":
                return redirect("/Teacher")
            return redirect("/Account")
        return func(*kwargs, **args)
    return check_sub_exists

#User is verified with a student Id, so don't allow them to
#access things that someone with a student id can't
def check_sub_account_exists(func):
    @wraps(func)
    def check_sub_not_exists(*kwargs, **args):
        if session.get("sub_account_id") != None:
            return redirect("/Subaccount")
        return func(*kwargs, **args)
    return check_sub_not_exists

#Login User
@login_register.route('/Login', methods=["GET", "POST"])
@check_user_id_exists
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        return LoginRegisterHandler.login(request)

#Register home page
@login_register.route('/Register', methods=["GET", "POST"])
@check_user_id_exists
def register():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == "POST":
        return LoginRegisterHandler.register(request)
    
#Logout a user
@login_register.route("/Logout", methods=["GET"])
@check_user_id_not_exists
def logout():
    if request.method == "GET":
        return LoginRegisterHandler.logout(request)

#Home page
@login_register.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")

#Get the account for a parent
@login_register.route("/Account", methods=["GET", "POST"])
@check_sub_account_exists
@check_user_id_not_exists
def account():
    if request.method == "GET":
        sub_accounts=get_stu_accounts_main(session.get("user_id")).stu_accounts
        return render_template("account.html", sub_accounts=sub_accounts)
    if request.method == "POST":
        return LoginRegisterHandler.post_sub_account(request)

#Get the page for a teacher based on user id
@login_register.route("/Teacher", methods=["GET", "POST"])
@check_sub_account_exists
@check_user_id_not_exists
def teacher_account():
    if request.method == "GET":
        classes = get_teacher_classes(session.get("user_id")).class_information
        sub_accounts=get_stu_accounts_teacher(session.get("user_id")).stu_accounts
        return render_template("teacher_portal.html", sub_accounts=sub_accounts, classes=classes)
    if request.method == "POST":
        return LoginRegisterHandler.add_teacher_to_student_account(request)

#Update or delete the student account
@login_register.route("/Subaccount/<sub_account_id>", methods=["POST", "GET"])
@check_user_id_not_exists
@check_sub_account_exists
def update_sub_account(sub_account_id):
    #UPDATE
    if request.method == "POST":
        return LoginRegisterHandler.put_sub_account(request, sub_account_id)
    #DELETE
    if request.method == "GET":
        return LoginRegisterHandler.del_sub_account(sub_account_id)

#Login to the student account
@login_register.route("/Subaccount/Login/<sub_account_id>", methods=["GET"])
@check_user_id_not_exists
@check_sub_account_exists
def sub_account_login(sub_account_id):
    if request.method == "GET":
        session["sub_account_id"] = sub_account_id
        sacct = get_stu_account(sub_account_id).stu_account
        session["sub_account_information"] = sacct
        return redirect(url_for("login_register.sub_account"))
        
#Acess the logged in student account
@login_register.route("/Subaccount", methods=["GET"])
@check_user_id_not_exists
@check_sub_account_not_exists
def sub_account():
    if request.method == "GET":
        sub_account_id = session.get("sub_account_id")
        #Get information about the beedle to register information
        current_date = datetime.date.today().isoformat()
        beedle_questions = get_beedle_results(sub_account_id, current_date).questions
        completed_beedle = len(beedle_questions) == 5
        number_correct = len([b for b in beedle_questions if b.get("answered_correctly") == True])
        return render_template("sub_account.html", completed_beedle=completed_beedle, number_correct=number_correct)
    
@login_register.route("/clear_subaccount_session", methods=["POST"])
@check_user_id_not_exists
def clear_sub_account_session():
    if request.method == "POST":
        # Clear the sub_account_id and related information from session
        if "sub_account_id" in session:
            session.pop("sub_account_id")
        if "sub_account_information" in session:
            session.pop("sub_account_information")
        return {'success': True}, 200
