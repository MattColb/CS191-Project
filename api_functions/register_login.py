from db_functions.account.login import *
from db_functions.account.register import *
from api_functions.jwt_verification import jwt_creation
import json
import hashlib
import os

ddb_table_name = os.getenv("DYNAMODB_TABLE_NAME")

def register_handler(event, context):
    """
    Body must contain:
    username: str
    password: str
    email_address: str
    
    
    """
    body = json.loads(event.get("body"))
    username = body.get("username")
    email_address = body.get("email_address")
    password = body.get("password")
    if not (username and email_address and password):
        return {
            "statusCode":400,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Not all parameters where provided"})
        }
    
    #Think about salt
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user_id, success, error_message = register_account(username, hashed_password, email_address, ddb_table_name)

    if not success:
        return {
            "statusCode":409,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Account already exists"})
        }


    jwt_token = jwt_creation({"user_id":user_id})

    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*",
            "Set-Cookie":f"user_jwt={jwt_token}; HttpOnly; Secure"
        },
        "body":json.dumps({"Status":"Successfully Created account"})
    }

def login_handler(event, context):
    qsp = event.get("queryStringParameters")
    username = qsp.get("username")
    password = qsp.get("password")

    if not (username and password):
        return {
            "statusCode":400,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Not all parameters where provided"})
        }

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    user_id, success, error_message = login_account(username, hashed_password, ddb_table_name)

    if not success:
        return {
            "statusCode":401,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Login was not successful"})
        }

    jwt_token = jwt_creation({"user_id":user_id})
    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*",
            "Set-Cookie":f"user_jwt={jwt_token}; HttpOnly; Secure"
        },
        "body":json.dumps({"Status":"Successfully Logged In", "username":username})
    }