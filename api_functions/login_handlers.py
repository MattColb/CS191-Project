import json
import os
import uuid
import hashlib
import boto3

"""
Relevant Login information:

User ID
Username
Password
Account Type

All of this should come later:
Parent Email(s)?
Connected School account (teacher email?)
Relevant Student IDs


"""

def create_account_handler(event, context):
    ddb_table_name = os.getenv("DYNAMODB_TABLE_NAME")
    user_id = str(uuid.uuid4())
    username = ""
    account_type = ""
    password = ""
    #Think about salt
    hashed_passoword = hashlib.sha256(password.encode()).hexdigest()
    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*"
        },
        "body":json.dumps({"Status":"Successfully Created account", "user_id":user_id})
    }

def login_handler(event, context):
    pass

def update_account_handler(event, context):
    pass

def delete_account_handler(event, context):
    pass