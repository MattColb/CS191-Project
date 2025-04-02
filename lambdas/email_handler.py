import json
import boto3
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from buzzy_bee_db.account.stu_account import get_stu_accounts

# Consume the UserID from the SQS Queue
# Send out a verification email with the link to the verification endpoint in the website

sqs = boto3.client("sqs")

API_KEY = os.getenv("EMAIL_API_KEY")
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = API_KEY
SENDER = os.getenv("SENDER_EMAIL")
connection_string = os.getenv("MONGO_CONNECTION_STRING")


def handler(event, context):
    records = event.get("Records")
    if not isinstance(records, list):
        return

    for record in records:
        message = record.get("body")
        verification_info = json.loads(message)
        user_id = verification_info.get("UserID")
        email = verification_info.get("email")
        
        student_accounts = get_stu_accounts(user_id)

        for student in student_accounts:
            #Get information
            #
            pass
            send_email(email)
        


def send_email(email):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email, "name": "User"}],
        subject="Verify Your Email",
        html_content=f"<p>THIS IS WHERE SPECIFIC INFORMATION WOULD GO</p>",
        sender={"email": SENDER, "name": "Buzzy Bee"}
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Exception when sending email: {e}")
        
    return