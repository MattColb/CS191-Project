from flask import Blueprint, render_template, abort, request, redirect, url_for
from jinja2 import TemplateNotFound
from .helper_functions.login_register import LoginRegisterHandler
from buzzy_bee_db.mongo_init import test

login_register = Blueprint('login_register', __name__,
                        template_folder='templates')

@login_register.route('/login')
def login():
    if request.method == "GET":
        try:
            return render_template('login.html')
        except TemplateNotFound:
            abort(404)
    if request.method == "POST":
        return LoginRegisterHandler.login(request)

@login_register.route('/register')
def register():
    if request.method == 'GET':
        try:
            return render_template('register.html')
        except TemplateNotFound:
            abort(404)
    if request.method == "POST":
        return LoginRegisterHandler.register(request)
    
@login_register.route("/logout")
def logout():
    if request.method == "POST":
        return redirect("/")

@login_register.route('/')
def index():
    if request.method == "GET":
        return test()
        try:
            return render_template('index.html')
        except TemplateNotFound:
            abort(404)