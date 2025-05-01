import os
from dotenv import load_dotenv
from pymongo import MongoClient

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

def get_all_students():
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Students"]

        students = list(collection.find())

        return students
    
def update_verification_and_weekly_updates(user_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Users"]
        # Update the user document to set verified and weekly_updates to True
        result = collection.update_one(
            {"user_id": user_id},
            {"$set": {"verified": True, "weekly_updates": True}}
        )

        return result
