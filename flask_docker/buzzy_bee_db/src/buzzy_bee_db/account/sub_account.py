from .sub_account_response import GetSubAccounts, CreateSubAccount
from ..db_response import DBResponse
import os
from dotenv import load_dotenv
from uuid import uuid4
from pymongo import MongoClient

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

def get_sub_accounts(user_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Users"]
        query = collection.find({"user_id":user_id})
        list_query = query.to_list()
        sub_accounts = list_query[0]["sub_accounts"]
        return GetSubAccounts(success=True, sub_accounts=sub_accounts)

def create_sub_account(user_id, username):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Users"]
        sub_account_id = str(uuid4())

        new_sub_account = {
            "sub_account_id": sub_account_id,
            "sub_account_username": username,
            "name": "",
            "score_in_math": 0,
            "math_questions_answered": []
        }

        collection.update_one(
            {"user_id": user_id},
            {"$push": {"sub_accounts": new_sub_account}}
        )
        return CreateSubAccount(sub_account_id=sub_account_id, success=True)

def delete_sub_account(user_id, sub_account_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Users"]
        collection.update_one(
            {"user_id":user_id},
            {"$pull":{"sub_accounts":{"sub_account_id":sub_account_id}}}
        )
        return DBResponse(success=True)

"""
# Update subaccount info
def update_sub_account(user_id, sub_account_id, name=None, score_in_math=None):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Users"]

        update_fields = {}
        if name:
            update_fields["sub_accounts.$.name"] = name
        if score_in_math is not None:
            update_fields["sub_accounts.$.score_in_math"] = score_in_math

        result = collection.update_one(
            {"user_id": user_id},
            {"$set": update_fields},
            array_filters=[{"elem.sub_account_id": sub_account_id}]
        )

        print(result)
        if result.matched_count > 0:
            return DBResponse(success=True)
        return DBResponse(success=False, message="Sub-account not found")

# Add a question answered buy subaccount user
def add_question_answered(user_id, sub_account_id, question_id, time_taken, correct):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Users"]

        question_data = {
            "question_id": question_id,
            "time_taken": time_taken,
            "correct": correct
        }

        result = collection.update_one(
            {"user_id": user_id, "sub_accounts.sub_account_id": sub_account_id},
            {"$push": {"sub_accounts.$.math_questions_answered": question_data}}
        )

        if result.matched_count > 0:
            return DBResponse(success=True)
        return DBResponse(success=False, message="Sub-account or question not found")

# Adjust Math Score
def adjust_score(user_id, sub_account_id, score):

"""