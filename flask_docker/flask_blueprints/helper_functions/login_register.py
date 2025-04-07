from flask import request, session, url_for, flash, redirect
from buzzy_bee_db.account.main_account import register as parent_register, login as parent_login
from buzzy_bee_db.account.stu_account import create_stu_account, delete_sub_account, update_stu_account
from buzzy_bee_db.account.teacher_account import register as teacher_register, login as teacher_login
from hashlib import sha256
import os
from dotenv import load_dotenv
import json

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

def hash_password(password):
    new_password = ""
    new_password = sha256(str.encode(new_password)).hexdigest()
    return new_password

class LoginRegisterHandler:
    @staticmethod
    def login(request):
        username = request.form.get("username")
        password = request.form.get("password")
        password = hash_password(password)

        account_type = request.form.get("account_type", "parent")

        if None in [username, password]:
            flash("Please enter all fields")
            return redirect(url_for("login_register.login", _method="GET"))

        if account_type == "teacher":
            response = teacher_login(username=username, password=password)
        else:
            response = parent_login(username=username, password=password)
        if response.success == False:
            flash(response.message)
            return redirect(url_for("login_register.login", _method="GET"))

        session["user_id"] = response.user_id
        return redirect(url_for("login_register.account", _method="GET"))

    @staticmethod
    def register(request):
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        password = hash_password(password)

        account_type = request.form.get("account_type", "parent")
        
        if None in [email, username, password]:
            flash("Please enter all fields")
            return redirect(url_for("login_register.register", _method="GET"))

        if account_type == "teacher":
            response = teacher_register(username=username, email=email, password=password)
        else:
            response = parent_register(username=username, email=email, password=password)
        if response.success == False:
            flash(response.message)
            return redirect(url_for("login_register.register", _method="GET"))
        session["user_id"] = response.user_id

        # Add the user to a queue to send them a verification email
        if os.getenv("SQS_QUEUE_URL"):
            import boto3
            queue_url = os.getenv("SQS_QUEUE_URL")
            sqs = boto3.client("sqs")
            message = json.dumps({"UserID": response.user_id, "email":email})
            sqs.send_message(QueueUrl=queue_url, MessageBody=message)

        return redirect(url_for("login_register.account", _method="GET"))

    @staticmethod
    def logout(request):
        if session.get("user_id") != None:
            session.pop("user_id")
        if session.get("sub_account_id") != None:
            session.pop("sub_account_id")
        return redirect("/")

    @staticmethod
    def post_sub_account(request):
        sub_account_name = request.form.get("sub_account_name")

        user_id = session.get("user_id")

        if sub_account_name == None:
            flash("Please enter all fields")
            return redirect(url_for("login_register.account", _method="GET"))

        response = create_stu_account(user_id, sub_account_name)
        if response.success == False:
            flash(response.message)
            return redirect(url_for("login_register.account", _method="GET"))
        return redirect(url_for("login_register.account", _method="GET"))

    @staticmethod
    def del_sub_account(sub_account_id):
        user_id = session.get("user_id")
        
        response = delete_sub_account(user_id, sub_account_id)

        if response.success == False:
            flash(response.message)
        return redirect(url_for("login_register.account", _method="GET"))

    @staticmethod
    def put_sub_account(request, sub_account_id):
        user_id = session.get("user_id")
        
        sub_account_name = request.form.get("sub_account_name")
        if sub_account_name == None:
            flash("Please enter all fields")
            return redirect(url_for("login_register.account", _method="GET"))
        response = update_stu_account(user_id, sub_account_id, sub_account_name)

        if response.success == False:
            flash(response.message)
        return redirect(url_for("login_register.account", _method="GET"))