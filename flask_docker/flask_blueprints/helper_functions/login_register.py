from flask import request, session, url_for, flash, redirect
from buzzy_bee_db.account.main_account import register as parent_register, login as parent_login
from buzzy_bee_db.account.stu_account import create_stu_account, delete_sub_account, update_stu_account, add_teacher
from buzzy_bee_db.account.teacher_account import register as teacher_register, login as teacher_login
from hashlib import sha256
import os
from dotenv import load_dotenv
import json

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

# Hash whatever is given
def hash_password(password):
    new_password = ""
    new_password = sha256(str.encode(new_password)).hexdigest()
    return new_password

class LoginRegisterHandler:
    @staticmethod
    def login(request):
        #Get user information
        username = request.form.get("username").lower()
        password = request.form.get("password")
        password = hash_password(password)

        account_type = request.form.get("account_type", "parent")
        # If not all fields, make them try again
        if None in [username, password]:
            flash("Please enter all fields")
            return redirect(url_for("login_register.login", _method="GET"))

        # If they are teacher, login as teacher
        if account_type == "teacher":
            response = teacher_login(username=username, password=password)
            session["user_id"] = response.teacher_id
            session["user_type"] = "teacher"
            if response.success == False:
                flash(response.message)
                return redirect(url_for("login_register.login", _method="GET"))
            return redirect(url_for("login_register.teacher_account", _method="GET"))
        #Otherwise login as parent
        else:
            response = parent_login(username=username, password=password)
            session["user_id"] = response.user_id
            session["user_type"] = "parent"
            if response.success == False:
                flash(response.message)
                return redirect(url_for("login_register.login", _method="GET"))
            return redirect(url_for("login_register.account", _method="GET"))

    @staticmethod
    def register(request):
        email = request.form.get("email")
        username = request.form.get("username").lower()
        password = request.form.get("password")
        password = hash_password(password)

        account_type = request.form.get("account_type", "parent")

        #Need all fields
        if None in [email, username, password]:
            flash("Please enter all fields")
            return redirect(url_for("login_register.register", _method="GET"))

        #Register as parent, teacher, or flash error
        if account_type == "teacher":
            response = teacher_register(username=username, email=email, password=password)
            session["user_id"] = response.teacher_id
            session["user_type"] = "teacher"
        else:
            response = parent_register(username=username, email=email, password=password)
            session["user_id"] = response.user_id
            session["user_type"] = "parent"
        if response.success == False:
            flash(response.message)
            return redirect(url_for("login_register.register", _method="GET"))

        # Add the user to a queue to send them a verification email
        if os.getenv("SQS_QUEUE_URL") and account_type != "teacher":
            import boto3
            queue_url = os.getenv("SQS_QUEUE_URL")
            sqs = boto3.client("sqs")
            message = json.dumps({"UserID": response.user_id, "email":email})
            sqs.send_message(QueueUrl=queue_url, MessageBody=message)
        #Render appropriate page
        if account_type == "teacher":
            return redirect(url_for("login_register.teacher_account", _method="GET"))
        return redirect(url_for("login_register.account", _method="GET"))

    #Logout user
    @staticmethod
    def logout(request):
        if session.get("user_id") != None:
            session.pop("user_id")
        if session.get("sub_account_id") != None:
            session.pop("sub_account_id")
        return redirect("/")

    #Create a sub account
    @staticmethod
    def post_sub_account(request):
        sub_account_name = request.form.get("sub_account_name").lower()

        user_id = session.get("user_id")

        if sub_account_name == None:
            flash("Please enter all fields")
            return redirect(url_for("login_register.account", _method="GET"))

        response = create_stu_account(user_id, sub_account_name)
        if response.success == False:
            flash(response.message)
            return redirect(url_for("login_register.account", _method="GET"))
        return redirect(url_for("login_register.account", _method="GET"))

    #Delete a sub account
    @staticmethod
    def del_sub_account(sub_account_id):
        user_id = session.get("user_id")
        
        response = delete_sub_account(user_id, sub_account_id)

        if response.success == False:
            flash(response.message)
        return redirect(url_for("login_register.account", _method="GET"))

    #Update a sub account with information
    @staticmethod
    def put_sub_account(request, sub_account_id):
        user_id = session.get("user_id")
        
        sub_account_name = request.form.get("sub_account_name")
        if sub_account_name == None:
            flash("Please enter all fields")
            return redirect(url_for("login_register.account", _method="GET"))
        response = update_stu_account(sub_account_id, sub_account_name)

        if response.success == False:
            flash(response.message)
        return redirect(url_for("login_register.account", _method="GET"))
    
    #Add a teacher to a student account
    @staticmethod
    def add_teacher_to_student_account(request):
        teacher_name = request.form.get("teacher_name").lower()
        student_account_id = request.form.get("student_id")

        if None in [teacher_name, student_account_id]:
            flash("Please enter all fields")
            return redirect(url_for("login_register.account", _method="GET"))

        db_response = add_teacher(student_account_id, teacher_name)
        if db_response.success==True:
            return redirect(url_for("login_register.account", _method="GET"))
        else:
            flash("That teacher doesn't exist")
            return redirect(url_for("login_register.account", _method="GET"))