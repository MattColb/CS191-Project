import os
import json
from buzzy_bee_db.account.sub_account import *
from jwt_verification import jwt_verification_retrieval, jwt_creation

ddb_table_name = os.getenv("DYNAMODB_TABLE_NAME")

# Maybe set the JWT here so that it can't have a sub user id
def api_get_sub_accounts(event, context):
    success, payload = jwt_verification_retrieval(event)
    if not success or payload.get("user_id") == None:
        return {
            "statusCode":400,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Not all parameters where provided"})
        }
    
    sub_users_response = get_sub_accounts(payload.get("user_id"), ddb_table_name)

    if not sub_users_response.success:
        return {
            "statusCode":401,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Issues getting the sub users"})
        }

    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*",
        },
        "body":json.dumps({"Status":"Successfully gathered users", "users":sub_users_response.users})
    }

def api_post_sub_accounts(event, context):
    success, payload = jwt_verification_retrieval(event)
    if not success or payload.get("user_id") == None:
        return {
            "statusCode":400,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Not all parameters where provided"})
        }

    body = json.loads(event.get("body"))
    sub_account_name = body.get("sub_account_name")
    sub_account_grade = body.get("sub_account_grade")

    sub_users_response = create_sub_account(payload.get("user_id"), ddb_table_name, sub_account_name, sub_account_grade)

    if not sub_users_response.success:
        return {
            "statusCode":401,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Issues getting the sub users"})
        }

    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*",
        },
        "body":json.dumps({"Status":"Successfully Added User"})
    }


def api_put_sub_accounts(event, context):
    success, payload = jwt_verification_retrieval(event)
    if not success or payload.get("user_id") == None:
        return {
            "statusCode":400,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Not all parameters where provided"})
        }

    body = json.loads(event.get("body"))
    sub_account_name = body.get("sub_account_name")
    sub_account_grade = body.get("sub_account_grade")
    sub_account_id = body.get("sub_account_id")

    sub_users_response = update_sub_account(payload.get("user_id"), ddb_table_name, sub_account_id, sub_account_new_name=sub_account_name, sub_account_new_grade=sub_account_grade)

    if not sub_users_response.success:
        return {
            "statusCode":401,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Issues getting the sub users"})
        }

    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*",
        },
        "body":json.dumps({"Status":"Successfully Updated User"})
    }


def api_delete_sub_accounts(event, context):
    success, payload = jwt_verification_retrieval(event)
    if not success or payload.get("user_id") == None:
        return {
            "statusCode":400,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Not all parameters where provided"})
        }

    body = json.loads(event.get("body"))
    sub_user_id = body.get("sub_user_id")

    sub_users_response = delete_sub_account(payload.get("user_id"), ddb_table_name, sub_user_id)

    if not sub_users_response.success:
        return {
            "statusCode":401,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Issues deleting the sub user"})
        }

    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*",
        },
        "body":json.dumps({"Status":"Successfully deleted the sub user"})
    }

def api_login_sub_account(event, context):
    success, payload = jwt_verification_retrieval(event)
    if not success or payload.get("user_id") == None:
        return {
            "statusCode":400,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Not all parameters where provided"})
        }
    
    payload.pop("sub_user_id", None)

    body = json.loads(event.get("body"))
    sub_user_id = body.get("sub_user_id", None)

    if sub_user_id == None:
        return {
            "statusCode":400,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Not all parameters where provided"})
        }

    payload["sub_user_id"] = sub_user_id

    jwt_token = jwt_creation(payload)

    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*",
            "Set-Cookie":f"user_jwt={jwt_token}; HttpOnly; Secure"
        },
        "body":json.dumps({"Status":"Successfully Logged into sub account"})
    }

def api_logout_sub_account(event, context):
    success, payload = jwt_verification_retrieval(event)
    if not success or payload.get("user_id") == None:
        return {
            "statusCode":400,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*",
            },
            "body":json.dumps({"Status":"Not all parameters where provided"})
        }

    payload.pop("sub_user_id", None)

    jwt_token = jwt_creation(payload)

    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*",
            "Set-Cookie":f"user_jwt={jwt_token}; HttpOnly; Secure"
        },
        "body":json.dumps({"Status":"Successfully Logged out of sub account"})
    }