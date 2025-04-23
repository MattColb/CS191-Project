from flask import Blueprint, abort, request, redirect, url_for, render_template, session
from jinja2 import TemplateNotFound
from .helper_functions.login_register import LoginRegisterHandler
from buzzy_bee_db.account.stu_account import get_stu_accounts_main, get_stu_account, get_stu_accounts_teacher
from functools import wraps
from buzzy_bee_db.classes_content.classes_content import get_teacher_classes

login_register = Blueprint('login_register', __name__,
                        template_folder='templates')


# Can adjust as needed
def check_user_id_not_exists(func):
    @wraps(func)
    def check_id_exists(*kwargs, **args):
        if session.get("user_id") == None:
            return redirect("/Login")
        return func(*kwargs, **args)
        
    return check_id_exists

def check_user_id_exists(func):
    @wraps(func)
    def check_user_id_dne(*kwargs, **args):
        if session.get("user_id") != None:
            if session.get("user_type") == "teacher":
                return redirect("/Teacher")
            return redirect("/Account")
        return func(*kwargs, **args)
    return check_user_id_dne

def check_sub_account_not_exists(func):
    @wraps(func)
    def check_sub_exists(*kwargs, **args):
        if session.get("sub_account_id") == None:
            if session.get("user_type") == "teacher":
                return redirect("/Teacher")
            return redirect("/Account")
        return func(*kwargs, **args)
    return check_sub_exists

def check_sub_account_exists(func):
    @wraps(func)
    def check_sub_not_exists(*kwargs, **args):
        if session.get("sub_account_id") != None:
            return redirect("/Subaccount")
        return func(*kwargs, **args)
    return check_sub_not_exists

@login_register.route('/Login', methods=["GET", "POST"])
@check_user_id_exists
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        return LoginRegisterHandler.login(request)

@login_register.route('/Register', methods=["GET", "POST"])
@check_user_id_exists
def register():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == "POST":
        return LoginRegisterHandler.register(request)
    
@login_register.route("/Logout", methods=["GET"])
@check_user_id_not_exists
def logout():
    if request.method == "GET":
        return LoginRegisterHandler.logout(request)

@login_register.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")

@login_register.route("/Account", methods=["GET", "POST"])
@check_sub_account_exists
@check_user_id_not_exists
def account():
    if request.method == "GET":
        sub_accounts=get_stu_accounts_main(session.get("user_id")).stu_accounts
        return render_template("account.html", sub_accounts=sub_accounts)
    if request.method == "POST":
        return LoginRegisterHandler.post_sub_account(request)

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

@login_register.route("/Subaccount/Login/<sub_account_id>", methods=["GET"])
@check_user_id_not_exists
@check_sub_account_exists
def sub_account_login(sub_account_id):
    if request.method == "GET":
        session["sub_account_id"] = sub_account_id
        sacct = get_stu_account(sub_account_id).stu_account
        session["sub_account_information"] = sacct
        return redirect(url_for("login_register.sub_account"))
        

@login_register.route("/Subaccount", methods=["GET"])
@check_user_id_not_exists
@check_sub_account_not_exists
def sub_account():
    if request.method == "GET":
        return render_template("sub_account.html")