import os
import boto3
import json

# Query the MongoDB table to get all of the parents who have verified their emails
# Add them to the SQS Queue

sqs = boto3.client("sqs")

def handler(event, context):
    sqs_url = os.getenv("SQS_QUEUE_URL")
    mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")
    user_ids = ["ABC", "DEF", "GHI"] #These need to be queried from the mongo db
    for user in user_ids:
        message = json.dumps({"UserID":user["user_id"], "email":user["email"]})
        sqs.send_message(QueueUrl=sqs_url, MessageBody=message)