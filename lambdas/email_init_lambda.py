import os
import boto3
import json
from buzzy_bee_db.account.verification_notification import get_all_students

# Query the MongoDB table to get all of the parents who have verified their emails
# Add them to the SQS Queue

# sqs = boto3.client("sqs")

def handler(event, context):
    # sqs_url = os.getenv("SQS_QUEUE_URL")
    mongo_connection_string = "mongodb://buzzy_bee:buzz@34.193.60.33/buzzy_bee_db"
    student_ids = get_all_students(mongo_connection_string)
    for student in student_ids:
        message = json.dumps({"student_id":student["student_id"], "main_user_id":student["main_user_id"]})
        # sqs.send_message(QueueUrl=sqs_url, MessageBody=message)

if __name__ == "__main__":
    handler(None, None)