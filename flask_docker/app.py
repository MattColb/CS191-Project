import subprocess

subprocess.run("pip install --upgrade ./buzzy_bee_db".split(" "))
from flask import Flask, request, redirect
from pymongo import MongoClient
import os
from flask_blueprints.login_register import login_register

app = Flask(__name__)
app.register_blueprint(login_register)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
