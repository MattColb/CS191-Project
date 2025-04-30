import os
import boto3
import json
from buzzy_bee_db.account.verification_notification import get_all_students

# Query the MongoDB table to get all of the parents who have verified their emails
# Add them to the SQS Queue

sqs = boto3.client("sqs")

def handler(event, context):
    sqs_url = os.getenv("SQS_QUEUE_URL")
    student_ids = get_all_students()
    for student in student_ids:
        message = json.dumps({"student_id":student["student_id"], "main_user_id":student["main_user_id"]})
        sqs.send_message(QueueUrl=sqs_url, MessageBody=message)
