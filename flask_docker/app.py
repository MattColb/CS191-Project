""" import subprocess

subprocess.run("pip install --upgrade ./buzzy_bee_db".split(" "))
from flask import Flask, request, redirect
subprocess.run("pip install --upgrade pymongo".split(" "))
import os
from flask_blueprints.login_register import login_register
from flask_blueprints.math import math

app = Flask(__name__)
app.secret_key="TestSecret"
app.register_blueprint(login_register)
app.register_blueprint(math)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80) """


from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/sub_account')
def sub_account():
    return render_template('sub_account.html')

@app.route('/math')
def math():
    return render_template('math.html')

if __name__ == '__main__':
    app.run(debug=True)
