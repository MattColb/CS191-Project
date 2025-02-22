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
        collection.update_one(
            {"user_id":user_id},
            {"$push":{"sub_accounts": {"sub_account_id":sub_account_id, "sub_account_username":username}}}
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

#Needs to be updated
def update_sub_account(user_id, sub_account_id, sub_account_name):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Users"]
        result = collection.update_one(
            {"user_id": user_id},
            {"$set": {"sub_accounts.$[elem].sub_account_name": sub_account_name}},
            array_filters=[{"elem.sub_account_id": sub_account_id}]
        )
        print(result)
        if result.matched_count > 0:
            return DBResponse(success=True)
        return DBResponse(success=False)