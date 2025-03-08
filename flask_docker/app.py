import subprocess

subprocess.run("pip install --upgrade ./buzzy_bee_db".split(" "))
from flask import Flask, request, redirect
import os
from flask_blueprints.login_register import login_register
from flask_blueprints.math import math
from buzzy_bee_db.account.main_account import ping_db, conn_string

app = Flask(__name__)
app.secret_key="TestSecret"
app.register_blueprint(login_register)
app.register_blueprint(math)

# Add an endpoint that returns the result of pinging the DB
@app.route("/ping_db")
def ping_db_endpoint():
    return ping_db()

@app.route("/conn_string")
def conn_string_endpoint():
    return conn_string()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
