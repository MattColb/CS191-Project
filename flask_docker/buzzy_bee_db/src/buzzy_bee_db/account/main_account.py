import os
from pymongo import MongoClient
from dotenv import load_dotenv
from uuid import uuid4
from .main_account_response import MainAccountResponse

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

def login(username, password):
    pass

def register(username, password, email):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Users"]
        query = collection.find({"username":username})
        query = query.to_list()
        if len(query) != 0:
            return MainAccountResponse(success=False, message="There was already someone with that username")
        user_id = str(uuid4())
        response = collection.insert_one({
            "user_id":user_id,
            "username":username,
            "password":password,
            "email":email
        })
        print(response)
        return MainAccountResponse(success=True, user_id =user_id)

    

def logout():
    pass