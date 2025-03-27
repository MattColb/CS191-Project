import json
import boto3
import os

# Consume the UserID from the SQS Queue
# Send out a verification email with the link to the verification endpoint in the website

ses = boto3.client("ses")
sqs = boto3.client("sqs")

def handler(event, context):
    records = event.get("Records")
    if not isinstance(records, list):
        return
    
    SENDER = os.getenv("SENDER_EMAIL")
    connection_string = os.getenv("MONGO_CONNECTION_STRING")

    for record in records:
        message = record.get("body")
        verification_info = json.loads(message)
        user_id = verification_info.get("UserID")
        email = verification_info.get("email")
        response = ses.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [email]},
            Message={
                "Subject": {"Data": "Verify Your Email"},
                "Body": {
                    "This would be the body of the email. We would want to get some of this information from the mongo db"
                }
            }
        )