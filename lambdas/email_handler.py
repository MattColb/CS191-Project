import json
import boto3
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from buzzy_bee_db.account.stu_account import get_stu_accounts
from buzzy_bee_db.question_user.question_user import get_student_account_responses

from dotenv import load_dotenv

load_dotenv("../flask_docker/.env")
load_dotenv("../.env")

API_KEY = os.getenv("EMAIL_API_KEY")
if API_KEY != None:
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
        
        db_response = get_stu_accounts(user_id)

        if db_response.success == False:
            print(f"{user_id} was not able to be processed sucessfully")
            continue
        student_accounts = db_response.stu_accounts

        for student in student_accounts:
            student_id = student.get("student_id")
            #Get information (Mainly Question information)

            #Add in subject to question user
            question_information = get_question_information(student_id)
            print(question_information)

            #Snapshot their information
            q_information = create_db_snapshot(student, question_information)

            #Get all snapshots
            snapshots = get_snapshots(student_id)

            #Create graph (Matplotlib?)
            create_graph(snapshots)

            #Send Email with information
            send_email(email, q_information)
        


def send_email(email, test_information):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    email_content = str(test_information)

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email, "name": "User"}],
        subject="Verify Your Email",
        html_content=email_content,
        sender={"email": SENDER, "name": "Buzzy Bee"}
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Exception when sending email: {e}")
        
    return

def create_db_snapshot(student_information, question_information):
    from_student = []
    for key in from_student:
        question_information[key] = student_information.get(key)
    #snapshot

def get_question_information(student_id):
    subjects = ["MATH"]
    summary_information = dict()
    db_response = get_student_account_responses(student_id)
    if db_response.success == True:
        questions = db_response.responses
    else:
        return dict()
    for subject in subjects:
        subject_questions = [q for q in questions if q["subject"] == subject]
        subject_answered = len(subject_questions)
        subject_correct = len([q for q in subject_questions if q["answered_correctly"] == True])
        if subject_answered != 0:
            subject_percentage = round(subject_correct/subject_answered, 4) * 100
        else:
            subject_percentage = 0 

        summary_information[f"{subject}_answered"] = subject_answered
        summary_information[f"{subject}_correct"] = subject_correct
        summary_information[f"{subject}_percentage"] = subject_percentage

    return summary_information

def create_graph(snapshots):
    pass

def get_snapshots(student_id):
    pass

if __name__ == "__main__":
    event = {
        "Records":[
            {
                "body":'{"UserID":"5691d497-007d-4e54-bd98-73025634342d", "email":"colbertmatt12@gmail.com"}'
            }
        ]
    }
    context = ""
    handler(event, context)