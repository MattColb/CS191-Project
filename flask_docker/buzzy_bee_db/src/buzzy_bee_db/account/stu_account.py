from .stu_account_response import GetStuAccounts, CreateStuAccount, GetStuAccountResponses, RecordStuAccountResponse, GetStuAccount
from ..db_response import DBResponse
import os
from dotenv import load_dotenv
from uuid import uuid4
from pymongo import MongoClient

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

#STUDENT ACCOUNT

def get_stu_accounts(user_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Students"]

        student_accounts = list(collection.find({"main_user_id": user_id}, {"_id": 0}))

        if student_accounts:
            return GetStuAccounts(success=True, stu_accounts=student_accounts)
        return GetStuAccounts(success=False, message="No student accounts found for this main user", stu_accounts=student_accounts)

def create_stu_account(main_user_id, stu_username):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        students_collection = database["Students"]
        users_collection = database["Users"]

        # Check if username already exists
        query = students_collection.find({"stu_username": stu_username})
        query = query.to_list()
        if len(query) != 0:
            return CreateStuAccount(success=False, message="This username is already taken")
        
        student_id = str(uuid4())

        students_collection.insert_one({
            "student_id": student_id,
            "main_user_id": main_user_id,  # Reference to the main account
            "stu_username": stu_username,
            "name": stu_username, #For now
            "score_in_math": 0,
            "score_in_spelling": 0,
            "math_questions_answered": []
        })

        # Reference to the main account
        users_collection.update_one(
            {"user_id": main_user_id},
            {"$push": {"students": student_id}}
        )

        return CreateStuAccount(success=True, student_id=student_id)


def delete_sub_account(main_user_id, student_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        students_collection = database["Students"]
        users_collection = database["Users"]

        #???
        result = students_collection.delete_one({"student_id": student_id, "main_user_id": main_user_id})

        if result.deleted_count > 0:
            # Remove student reference from the main account
            users_collection.update_one(
                {"user_id": main_user_id},
                {"$pull": {"students": student_id}}
            )
            return DBResponse(success=True)
        return DBResponse(success=False, message="Student account not found")

def update_stu_account(main_user_id, student_id, name=None, score_in_math=None, score_in_spelling=None):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        students_collection = database["Students"]

        update_fields = {}
        if name:
            update_fields["name"] = name
        if score_in_math is not None:
            update_fields["score_in_math"] = score_in_math
        if score_in_spelling is not None:
            update_fields["score_in_spelling"] = score_in_spelling

        result = students_collection.update_one(
            {"student_id": student_id, "main_user_id": main_user_id},
            {"$set": update_fields}
        )

        if result.matched_count > 0:
            return DBResponse(success=True)
        return DBResponse(success=False, message="Student account not found")

def get_stu_account(main_user_id, student_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Students"]

        student_doc = collection.find_one(
            {"student_id": student_id, "main_user_id": main_user_id}, {"_id": 0}
        )

        if not student_doc:
            return GetStuAccount(success=False, message="Student account not found")
        return GetStuAccount(success=True, stu_account=student_doc)