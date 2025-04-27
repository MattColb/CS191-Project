import subprocess

subprocess.run("pip install --upgrade ./buzzy_bee_db".split(" "))
from flask import Flask
from flask_blueprints.login_register import login_register
from flask_blueprints.math_funcs import math
from flask_blueprints.spelling import spelling
from flask_blueprints.writing import writing
from flask_blueprints.verification import verification
from flask_blueprints.classes import classes
from flask_blueprints.beedle import beedle

app = Flask(__name__)
app.secret_key="TestSecret"
app.register_blueprint(login_register)
app.register_blueprint(math)
app.register_blueprint(spelling)
app.register_blueprint(writing)
app.register_blueprint(verification)
app.register_blueprint(classes)
app.register_blueprint(beedle)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
