import json
import os
import uuid
import hashlib
import boto3
from jwt_verification import *


ddb_client = boto3.client("dynamodb")
ddb_table_name = os.getenv("DYNAMODB_TABLE_NAME")

def create_account_handler(event, context):
    user_id = str(uuid.uuid4())
    body = json.loads(event.get("body"))
    username = body.get("username")
    account_type = body.get("account_type")
    password = body.get("password")
    #Think about salt
    hashed_passoword = hashlib.sha256(password.encode()).hexdigest()

    # Check if username exists
    response = ddb_client.query(
        TableName=ddb_table_name,
        IndexName="username-index",
        KeyConditionExpression='username = :username',
        ExpressionAttributeValues={
            ':username': {'S': username}
        }
    )
    if response["Count"] > 0:
        return {
        "statusCode":400,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*"
        },
        "body":json.dumps({"Status":"Account could not be created"})
    }

    # Post it to a db
    ddb_client.put_item(TableName=ddb_table_name, Item = {
        "user_id":{"S":user_id},
        "username":{"S":username},
        "account_type":{"S":account_type},
        "password":{"S":hashed_passoword}
    })
    jwt_token = jwt_creation({"user_id":user_id})
    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*",
            "Set-Cookie":f"user_jwt={jwt_token}; HttpOnly; Secure"
        },
        "body":json.dumps({"Status":"Successfully Created account", "user_id":user_id})
    }

def login_handler(event, context):
    qsp = event.get("queryStringParameters")
    username = qsp.get("username")
    password = qsp.get("password")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    response = ddb_client.query(
        TableName=ddb_table_name,
        IndexName="username-index",
        KeyConditionExpression='username = :username',
        ExpressionAttributeValues={
            ':username': {'S': username}
        }
    )
    if response["Count"] != 1:
        return {
            "statusCode":400,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*"
            },
            "body":json.dumps({"Status":"Account could not be logged in"})
        }
    if response["Items"][0]["password"]["S"] != hashed_password:
        return {
            "statusCode":400,
            "headers":{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin":"*"
            },
            "body":json.dumps({"Status":"Account could not be logged in"})
        }
    user_id = response["Items"][0]["user_id"]["S"]
    jwt_token = jwt_creation({"user_id":user_id})
    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*",
            "Set-Cookie":f"user_jwt={jwt_token}; HttpOnly; Secure"
        },
        "body":json.dumps({"Status":"Successfully Logged In", "username":username, "user_id":user_id})
    }

def update_account_handler(event, context):
    # get jwt and parse it to get the user id
    jwt = ""
    valid_user_keys = ["username", "password"]

    jwt_payload = jwt_payload_retrieval(jwt)
    user_id = jwt_payload.get("user_id")
    if user_id == None:
        return "Error"
    #Parse out the body and validate that they can modify everything that they want to
    body = json.loads(event.get("body"))
    real_put_dict = dict()
    for (key, value) in body.items():
        if key == "password":
            real_put_dict["password"] = hashlib.sha256(value.encode()).hexdigest()
        if key in valid_user_keys:
            real_put_dict[key] = value

    #Put the items based on the new values
    ddb_client.put_item(
        TableName=ddb_table_name,
        Key={"user_id":{"S":user_id}},
        # This is likely wrong
        AttributeUpates=real_put_dict
    )
    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*"
        },
        "body":json.dumps({"Status":"Successfully Updated User"})
    }
    

def delete_account_handler(event, context):
    jwt = ""
    jwt_payload = jwt_payload_retrieval(jwt)
    user_id = jwt_payload.get("user_id")
    if user_id == None:
        return "Error"
    ddb_client.delete_item(TableName=ddb_table_name, Key={"user_id", user_id})
    # Remove the JWT from client
    pass