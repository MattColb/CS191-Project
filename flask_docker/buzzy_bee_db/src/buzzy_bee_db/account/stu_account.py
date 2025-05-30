from .stu_account_response import GetStuAccounts, CreateStuAccount, GetStuAccountResponses, RecordStuAccountResponse, GetStuAccount
from ..db_response import DBResponse
import os
from dotenv import load_dotenv
from uuid import uuid4
from pymongo import MongoClient

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

#STUDENT ACCOUNT

def get_stu_accounts_main(user_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Students"]

        student_accounts = list(collection.find({"main_user_id": user_id}, {"_id": 0}))

        if student_accounts:
            return GetStuAccounts(success=True, stu_accounts=student_accounts)
        return GetStuAccounts(success=False, message="No student accounts found for this main user", stu_accounts=student_accounts)

def get_stu_accounts_teacher(teacher_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Students"]

        student_accounts = list(collection.find({"teacher_ids": teacher_id}, {"_id": 0}))

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
            "teacher_ids":[],
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

def update_stu_account(student_id, name=None, score_in_math=None, score_in_spelling=None):
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
            {"student_id": student_id},
            {"$set": update_fields}
        )

        if result.matched_count > 0:
            return DBResponse(success=True)
        return DBResponse(success=False, message="Student account not found")

def get_stu_account(student_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Students"]

        student_doc = collection.find_one(
            {"student_id": student_id}, {"_id": 0}
        )

        if not student_doc:
            return GetStuAccount(success=False, message="Student account not found")
        return GetStuAccount(success=True, stu_account=student_doc)
    
def get_stu_accounts_list(student_ids):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        students = database["Students"]

        all_students = list(students.find({"student_id":{"$in": students}}))

        GetStuAccounts(success=True, stu_accounts=all_students)

def add_teacher(student_id, teacher_name):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        teachers = database["Teachers"]

        # Check if teacher exists
        query = teachers.find({"username": teacher_name})
        list_query = query.to_list()
        if len(list_query) != 1:
           return DBResponse(success=False, message="That teacher doesn't exist")
        teacher_id = list_query[0].get("teacher_id")
    
        students = database["Students"]

        result_student = students.update_one(
            {"student_id": student_id},
            {"$push": {"teacher_ids":teacher_id}}
        )

        result_teacher = teachers.update_one(
            {"teacher_id":teacher_id},
            {"$push":{"students":student_id}}
        )

        if result_student.matched_count > 0 and result_teacher.matched_count > 0:
            return DBResponse(success=True)
        return DBResponse(success=False, message="Student or teacher account not found")