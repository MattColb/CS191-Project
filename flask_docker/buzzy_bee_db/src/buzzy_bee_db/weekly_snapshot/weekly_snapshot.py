import os
from pymongo import MongoClient
from dotenv import load_dotenv
from uuid import uuid4
from datetime import datetime
from .weekly_snapshot_response import WeeklySnapshotResponse

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

# Records a weekly snapshot for a student account
def record_snapshot(response_data):

    """
    Records a weekly snapshot for a student account.
    Example:
    response_data = {
    "student_account_id": "stu_add",  # Unique ID for student
    "timestamp_utc": datetime.utcnow(),  # Time of snapshot
    "questions_attempted": 3,  # Number of questions attempted this week
    "correct_answers": 3,  # Correct answers
    "average_time_per_question": 3.3,  # Average time per question
    "rating_change": +3,  # Any change in student rating
    "notes": "..."  # Additional comments/notes
    }
    """

    required_fields = ["student_account_id", "timestamp_utc"]
    for field in required_fields:
        if field not in response_data:
            return WeeklySnapshotResponse(success=False, message=f"Missing required field: {field}")

    # Add snapshot_id
    response_data["snapshot_id"] = str(uuid4())

    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["WeeklySnapshot"]

        collection.insert_one(response_data)
        return WeeklySnapshotResponse(success=True, response_id=response_data["snapshot_id"], message="Snapshot recorded successfully")


# Retrieves all weekly snapshots for a given student_account_id
def get_snapshots(student_account_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["WeeklySnapshot"]

        snapshots = list(collection.find({"student_account_id": student_account_id}, {"_id": 0}).sort("timestamp_utc", -1))
        return WeeklySnapshotResponse(success=True, responses=snapshots, message="Snapshots retrieved successfully")

# Retrieves the latest weekly snapshot for a given student_account_id
def get_latest_snapshot(student_account_id, snapshot_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["WeeklySnapshot"]

        snapshot = collection.find({"student_account_id": student_account_id}).sort("timestamp_utc", -1).limit(1)
        if not snapshot:
            return WeeklySnapshotResponse(success=False, message="No snapshot found")
        
        return WeeklySnapshotResponse(success=True, response=snapshot, message="Latest snapshot retrieved successfully")

