from flask import request, session, url_for, flash, redirect
from buzzy_bee_db.account.main_account import register, login
from buzzy_bee_db.account.sub_account import create_sub_account, delete_sub_account #, update_sub_account
from hashlib import sha256

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

        if None in [username, password]:
            flash("Please enter all fields")
            return redirect(url_for("login_register.login", _method="GET"))

        response = login(username=username, password=password)
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
        
        if None in [email, username, password]:
            flash("Please enter all fields")
            return redirect(url_for("login_register.register", _method="GET"))

        response = register(username=username, email=email, password=password)
        if response.success == False:
            flash(response.message)
            return redirect(url_for("login_register.register", _method="GET"))
        session["user_id"] = response.user_id
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

        response = create_sub_account(user_id, sub_account_name)
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
        response = update_sub_account(user_id, sub_account_id, sub_account_name)

        if response.success == False:
            print("NO MATCHING")
            flash(response.message)
        return redirect(url_for("login_register.account", _method="GET"))