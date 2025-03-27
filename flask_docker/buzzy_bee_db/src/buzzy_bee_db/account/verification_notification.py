import os
from dotenv import load_dotenv
from pymongo import MongoClient

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

def get_users_to_email():
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Users"]
        email_users = collection.find({"verified":True, "weekly_updates":True}, {"user_id": 1, "email": 1})
        return list(email_users)
    
def update_verification_and_weekly_updates(user_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Users"]
        result = collection.update_one(
            {"user_id": user_id},
            {"verified":True, "weekly_updates":True}
        )

        return result
