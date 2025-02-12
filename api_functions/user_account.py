from db_functions.account.sub_accounts import *
import json
from api_functions.jwt_verification import jwt_verification_retrieval
import os

ddb_table_name = os.getenv("DYNAMODB_TABLE_NAME")

def get_sub_account_handler(event, context):


    pass

def post_sub_account_handler(event, context):
    jwt = ""
    valid, jwt_payload = jwt_verification_retrieval(event, jwt)
    if not valid:
        return None
        # Delete cookie and logout
    body = json.loads(event.get("body"))
    username = body.get("username")
    create_sub_account(jwt_payload.get("user_id"), username, ddb_table_name)
    pass

def put_sub_account_handler(event, context):
    pass

def delete_sub_account_handler(event, context):
    pass