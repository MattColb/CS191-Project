import json
import os
import boto3


def handler(event, context):
    ddb_table_name = os.getenv("DYNAMODB_TABLE_NAME")
    ddb_client = boto3.client("dynamodb")
    results = ddb_client.scan(
        TableName=ddb_table_name
    )
    all_items = json.dumps({"Status":results.get("Items")})
    return {
        "statusCode":200,
        "headers":{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin":"*"
        },
        "body":all_items
    }