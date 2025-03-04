import subprocess

# subprocess.run("pip install --upgrade ./buzzy_bee_db".split(" "))
from flask import Flask, request, redirect
import os
from flask_blueprints.login_register import login_register
from flask_blueprints.math import math

app = Flask(__name__)
app.secret_key="TestSecret"
app.register_blueprint(login_register)
app.register_blueprint(math)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
