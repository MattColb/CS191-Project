from flask import request, session

class LoginRegisterHandler:
    @staticmethod
    def login(request):
        pass

    @staticmethod
    def register(request):
        
        email = ""
        username = "" 
        password = ""
        
        session["logged_in"] = True

    @staticmethod
    def logout(request):
        pass