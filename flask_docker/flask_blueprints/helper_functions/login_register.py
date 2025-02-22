from flask import request, session, url_for, flash, redirect
from buzzy_bee_db.account.main_account import register

class LoginRegisterHandler:
    @staticmethod
    def login(request):
        pass

    @staticmethod
    def register(request):
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        
        if None in [email, username, password]:
            flash("Please enter all fields")
            return redirect(url_for("login_register.register", _method="GET"))

        response = register(username=username, email=email, password=password)
        if response.success == False:
            flash(response.message)
            return redirect(url_for("login_register.register", _method="GET"))
        return redirect(url_for("login_register.login", _method="GET"))

    @staticmethod
    def logout(request):
        pass