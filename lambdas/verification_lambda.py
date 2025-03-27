import json
import boto3
import os

# Consume the UserID from the SQS Queue
# Send out a verification email with the link to the verification endpoint in the website

ses = boto3.client("ses")

def handler(event, context):
    records = event.get("Records")
    if not isinstance(records, list):
        return
    
    SENDER = os.getenv("SENDER_EMAIL")
    verification_endpoint = os.getenv("VERIFICATION_ENDPOINT")
    
    for record in records:
        message = record.get("body")
        verification_info = json.loads(message)
        user_id = verification_info.get("UserID")
        email = verification_info.get("email")
        verification_url = verification_endpoint + f"?user_id={user_id}"
        #Should have access to anything we want from buzzy bee
        response = ses.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [email]},
            Message={
                "Subject": {"Data": "Verify Your Email"},
                "Body": {
                    "Html": {
                        "Data": f"""
                        <p>Click the link below to verify your email:</p>
                        <a href="{verification_url}">Verify Email</a>
                        <p>If you did not request this, please ignore.</p>
                        """
                    }
                }
            }
        )
