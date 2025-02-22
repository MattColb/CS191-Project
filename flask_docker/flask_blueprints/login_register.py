from flask import Blueprint, abort, request, redirect, url_for, render_template
from jinja2 import TemplateNotFound
from .helper_functions.login_register import LoginRegisterHandler

login_register = Blueprint('login_register', __name__,
                        template_folder='templates')

@login_register.route('/Login')
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
    
@login_register.route("/Logout")
def logout():
    if request.method == "POST":
        return redirect("/")

@login_register.route('/')
def index():
    if request.method == "GET":
        return render_template('index.html', )