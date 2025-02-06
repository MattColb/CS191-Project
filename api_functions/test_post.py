import json
import os
import boto3
import uuid

def handler(event, context):
    ddb_client = boto3.client("dynamodb")
    ddb_table_name = os.getenv("DYNAMODB_TABLE_NAME")
    response = ddb_client.put_item(
        TableName=ddb_table_name,
        Item = {
            "user_id":{"S":str(uuid.uuid4())},
            "username":{"S":event["queryStringParameters"]["username"]}
        }
    )
    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*"
        },
        "body":json.dumps({"Status": f"Write Completed!"})
    }