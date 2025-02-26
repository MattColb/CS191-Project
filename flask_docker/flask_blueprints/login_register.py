from flask import Blueprint, abort, request, redirect, url_for, render_template, session
from jinja2 import TemplateNotFound
from .helper_functions.login_register import LoginRegisterHandler
from buzzy_bee_db.account.sub_account import get_sub_accounts
from functools import wraps

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
            return redirect("/Account")
        return func(*kwargs, **args)
    return check_user_id_dne

def check_sub_account_not_exists(func):
    @wraps(func)
    def check_sub_exists(*kwargs, **args):
        if session.get("sub_account_id") == None:
            return redirect("/Account")
        return func(*kwargs, **args)
    return check_sub_exists

def check_sub_account_exists(func):
    @wraps(func)
    def check_sub_not_exists(*kwagrs, **args):
        if session.get("sub_account_id") != None:
            return redirect("/Subaccount")
        return func(*kwargs, **args)


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
        return render_template('register.html')
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
@check_user_id_exists
def account():
    if request.method == "GET":
        sub_accounts=get_sub_accounts(session.get("user_id")).sub_accounts
        return render_template("account.html", sub_accounts=sub_accounts)
    if request.method == "POST":
        return LoginRegisterHandler.post_sub_account(request)

@login_register.route("/Subaccount/<sub_account_id>", methods=["POST", "GET"])
@check_user_id_not_exists
def update_sub_account(sub_account_id):
    #UPDATE
    if request.method == "POST":
        return LoginRegisterHandler.put_sub_account(request, sub_account_id)
    #DELETE
    if request.method == "GET":
        return LoginRegisterHandler.del_sub_account(sub_account_id)

@login_register.route("/Subaccount/Login/<sub_account_id>", methods=["GET"])
@check_user_id_not_exists
def sub_account_login(sub_account_id):
    if request.method == "GET":
        session["sub_account_id"] = sub_account_id
        return redirect(url_for("login_register.sub_account"))
        

@login_register.route("/Subaccount", methods=["GET"])
def sub_account():
    if request.method == "GET":
        return render_template("sub_account.html")