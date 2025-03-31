import os
from pymongo import MongoClient
from dotenv import load_dotenv
from uuid import uuid4
from .teacher_account_response import TeacherAccountResponse

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

# TEACHER ACCOUNT

def login(username, password):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Teachers"]

        # Check if teacher exists
        query = collection.find({"username": username})
        list_query = query.to_list()
        if len(list_query) != 1:
            return TeacherAccountResponse(success=False, message="Please enter a valid teacher username")
        if password != list_query[0].get("password"):
            return TeacherAccountResponse(success=False, message="Incorrect password")
        teacher_id = list_query[0].get("teacher_id")

        return TeacherAccountResponse(success=True, teacher_id=teacher_id)


def register(username, password, email):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Teachers"]

        # Ensure unique username
        if collection.find_one({"username": username}):
            return TeacherAccountResponse(success=False, message="This username is already taken")

        teacher_id = str(uuid4())
        response = collection.insert_one({
            "teacher_id": teacher_id,
            "username": username,
            "password": password,
            "email": email,
            "students": []  # Store assigned student IDs here
        })

        return TeacherAccountResponse(success=True, teacher_id=teacher_id, students=[])
