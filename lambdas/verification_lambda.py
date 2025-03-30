import json
import boto3
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# Consume the UserID from the SQS Queue
# Send out a verification email with the link to the verification endpoint in the website

def handler(event, context):
    records = event.get("Records")
    if not isinstance(records, list):
        return
    
    SENDER = os.getenv("SENDER_EMAIL")
    verification_endpoint = os.getenv("VERIFICATION_ENDPOINT")
    api_key = os.getenv("EMAIL_API_KEY")

    config = sib_api_v3_sdk.Configuration()
    config.api_key['api-key'] = api_key
    
    for record in records:
        message = record.get("body")
        verification_info = json.loads(message)
        user_id = verification_info.get("UserID")
        email = verification_info.get("email")
        verification_url = verification_endpoint + f"?user_id={user_id}"
        #Should have access to anything we want from buzzy bee

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(config))

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email, "name": "User"}],
            subject="Verify Your Email",
            html_content=f"<p>Click <a href='{verification_url}'>here</a> to verify your email.</p>",
            sender={"email": SENDER, "name": "Buzzy Bee"}
        )

        try:
            api_instance.send_transac_email(send_smtp_email)
        except ApiException as e:
            print(f"Exception when sending email: {e}")
            continue