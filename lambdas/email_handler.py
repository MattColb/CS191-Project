import json
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from buzzy_bee_db.account.stu_account import get_stu_account
from buzzy_bee_db.account.main_account import get_main_account
from buzzy_bee_db.question_user.question_user import get_student_account_responses
from buzzy_bee_db.weekly_snapshot.weekly_snapshot import get_latest_snapshot, get_snapshots, record_snapshot
import matplotlib.pyplot as plt
from datetime import datetime
from email_html import create_html
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image
import io
import base64

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
        user_id = verification_info.get("main_user_id")
        student_id = verification_info.get("student_id")

        db_response = get_stu_account(student_id)

        if db_response.success == False:
            print(f"{student_id} was not able to be processed sucessfully")
            continue
        student = db_response.stu_account

        
        student_name = student.get("name")

        #Get information (Mainly Question information)
        previous_week_information = get_latest_snapshot(student_id)
        previous_week_information = previous_week_information.response

        #Add in subject to question user
        question_information = get_question_information(student_id, previous_week_information)

        #Snapshot their information
        weeks_information = create_db_snapshot(student, question_information)

        #Get all snapshots
        snapshots_response = get_snapshots(student_id)
        if snapshots_response.success == True:
            snapshots = snapshots_response.responses
        else:
            continue

        #Create graph to save in snapshot_graph.png
        create_graph(snapshots)

        main_user = get_main_account(user_id)

        main_user = main_user.user

        if main_user.get("weekly_updates"):
            email = main_user.get("email")
            #Send Email with information
            send_email(email, weeks_information, student_name, previous_week_information)

def create_image_bytes():
    image = Image.open("./image.png")
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="png")
    image_str = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
    return image_str

def send_email(email, current_week_info, student_name, previous_week_info):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    email_content = create_html(current_week_info, student_name, previous_week_info)

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email, "name": "User"}],
        subject="Buzzy Bee Weekly Update",
        html_content=email_content,
        sender={"email": SENDER, "name": "Buzzy Bee"},
        attachment=[
            {
                "content":create_image_bytes(),
                "content_id":"bee_image",
                "name":"bee_image.png"
            }
        ]
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Exception when sending email: {e}")
        
    return



def create_db_snapshot(student_information, question_information):
    question_information["student_account_id"] = student_information.get("student_id")
    question_information["timestamp_utc"] = datetime.isoformat(datetime.utcnow())
    for key in student_information:
        if key.startswith("score"):
            question_information[key] = student_information.get(key)
    record_snapshot(question_information)
    return question_information

def get_question_information(student_id, previous_snapshot):
    subjects = ["MATH", "SPELLING"]
    summary_information = dict()
    db_response = get_student_account_responses(student_id)
    if db_response.success == True:
        questions = db_response.responses
    else:
        return dict()
    #Limit to just questions answered since the last snapshot
    if previous_snapshot != None and len(previous_snapshot) != 0:
        previous_snapshot = previous_snapshot[0]
        questions = [question for question in questions if str(question.get("timestamp_utc")) > previous_snapshot.get("timestamp_utc")]
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
    # Create the plot
    fig, ax = plt.subplots()

    dates = [datetime.fromisoformat(snapshot.get("timestamp_utc")) for snapshot in snapshots]
    math = [snapshot.get("score_in_math", 0) for snapshot in snapshots]
    spelling = [snapshot.get("score_in_spelling", 0) for snapshot in snapshots]

    ax.plot(dates, math, label='Math')
    ax.plot(dates, spelling, label='Spelling')

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    ax.set_title('Student Progress over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Score Rating')

    # Add a legend
    ax.legend()

    # Rotate date labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    # Show the plot
    plt.savefig("./image.png")

if __name__ == "__main__":
    event = {
        "Records":[
            {
                "body":'{"main_user_id":"1fdc8c15-e04e-4eed-8002-fcf44ffa9d90", "student_id":"76396d82-ded9-4807-ac5a-8c7f3920ef57"}'
            }
        ]
    }
    context = ""
    handler(event, context)