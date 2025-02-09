import json
import os
import uuid
import hashlib
import boto3
from .jwt_verification import *


ddb_client = boto3.client("dynamodb")
ddb_table_name = os.getenv("DYNAMODB_TABLE_NAME")

def create_account_handler(event, context):
    user_id = str(uuid.uuid4())
    username = ""
    # Check if username exists
    account_type = ""
    password = ""
    #Think about salt
    hashed_passoword = hashlib.sha256(password.encode()).hexdigest()
    # Post it to a db
    ddb_client.post_item(TableName=ddb_table_name, Item = {
        "user_id":user_id,
        "username":username,
        "account_type":account_type,
        "password":hashed_passoword
    })

    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*"
        },
        "body":json.dumps({"Status":"Successfully Created account", "user_id":user_id})
    }

def login_handler(event, context):
    username = ""
    password = ""
    hashed_passoword = hashlib.sha256(password.encode()).hexdigest()
    # Check if account exists with username and hashed password
    # If it does, get the UUID associated with it
    user_id = str(uuid.uuid4())
    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*"
        },
        "body":json.dumps({"Status":"Successfully Logged In"})
    }

def update_account_handler(event, context):
    pass

def delete_account_handler(event, context):
    pass