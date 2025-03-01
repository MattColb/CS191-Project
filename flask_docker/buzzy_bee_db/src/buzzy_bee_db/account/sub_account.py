from .sub_account_response import GetSubAccounts, CreateSubAccount, GetSubAccountResponses, RecordSubAccountResponse
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
        user_doc = collection.find_one({"user_id": user_id})

        if user_doc and "sub_accounts" in user_doc:
            return GetSubAccounts(success=True, sub_accounts=user_doc["sub_accounts"])
        return GetSubAccounts(success=False, message="User not found or no sub-accounts")

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

        result = collection.update_one(
            {"user_id": user_id},
            {"$push": {"sub_accounts": new_sub_account}}
        )

        if result.matched_count > 0:
            return CreateSubAccount(sub_account_id=sub_account_id, success=True)
        return CreateSubAccount(success=False, message="User not found")

def delete_sub_account(user_id, sub_account_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Users"]
        result = collection.update_one(
            {"user_id": user_id},
            {"$pull": {"sub_accounts": {"sub_account_id": sub_account_id}}}
        )

        if result.modified_count > 0:
            return DBResponse(success=True)
        return DBResponse(success=False, message="Sub-account not found")

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
            {"user_id": user_id, "sub_accounts.sub_account_id": sub_account_id},
            {"$set": update_fields}
        )

        if result.matched_count > 0:
            return DBResponse(success=True)
        return DBResponse(success=False, message="Sub-account not found")

