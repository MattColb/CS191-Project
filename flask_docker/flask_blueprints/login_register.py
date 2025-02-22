from flask import Blueprint, abort, request, redirect, url_for, render_template, session
from jinja2 import TemplateNotFound
from .helper_functions.login_register import LoginRegisterHandler
from buzzy_bee_db.account.sub_account import get_sub_accounts

login_register = Blueprint('login_register', __name__,
                        template_folder='templates')

@login_register.route('/Login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        return LoginRegisterHandler.login(request)

@login_register.route('/Register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == "POST":
        return LoginRegisterHandler.register(request)
    
@login_register.route("/Logout", methods=["GET"])
def logout():
    if request.method == "GET":
        return LoginRegisterHandler.logout(request)

@login_register.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")

@login_register.route("/Subaccount", methods=["GET", "POST"])
def sub_account():
    if request.method == "GET":
        sub_accounts=get_sub_accounts(session.get("user_id")).sub_accounts
        return render_template("account.html", sub_accounts=sub_accounts)
    if request.method == "POST":
        return LoginRegisterHandler.post_sub_account(request)

@login_register.route("/Subaccount/<sub_account_id>", methods=["POST", "GET"])
def update_sub_account(sub_account_id):
    #UPDATE
    if request.method == "POST":
        return LoginRegisterHandler.put_sub_account(request, sub_account_id)
    #DELETE
    if request.method == "GET":
        return LoginRegisterHandler.del_sub_account(sub_account_id)

@login_register.route("/Subaccount/Login/<sub_account_id>", methods=["GET"])
def sub_account_login(sub_account_id):
    if request.method == "GET":
        session["sub_account_id"] = sub_account_id
        # Will redirect to sub account page
        return render_template("sub_account.html")

@login_register.route("/Subaccount/Logout", methods=["GET"])
def sub_account_logout():
    if request.method == "GET":
        session.pop("sub_account_id")
        return redirect("/Subaccount")