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
        #Get all user ids and emails where verified is True and weekly_updates is True
        users = collection.find({"verified": True, "weekly_updates": True})
        # Extract user_id and email from the cursor
        email_users = []
        for user in users:
            user_id = user.get("user_id")
            email = user.get("email")
            if user_id and email:
                email_users.append({"user_id": user_id, "email": email})
        # Return a list of dictionaries containing user_id and email
        return email_users
    
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
