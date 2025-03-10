import os
from pymongo import MongoClient
from dotenv import load_dotenv
from uuid import uuid4
from datetime import datetime
from .question_user_response import QuestionUserResponse

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

def record_question_response(sub_account_id, question_id, time_taken, percentile_time, question_rating_change, user_rating_change, answered_correctly):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["QuestionUser"]
        
        response_data = {
            "response_id": str(uuid4()),
            "sub_account_id": sub_account_id,
            "question_id": question_id,
            "time_taken": time_taken,
            "percentile_time": percentile_time,
            "answered_correctly": answered_correctly,
            "question_rating_change": question_rating_change,
            "user_rating_change": user_rating_change,
            "timestamp_utc": datetime.utcnow()
        }
        
        collection.insert_one(response_data)
        return QuestionUserResponse(success=True, response_id=response_data["response_id"], message="Response recorded successfully")

# Retrieves all question responses for a given sub_account_id
def get_sub_account_responses(sub_account_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["QuestionUser"]
        
        responses = list(collection.find({"sub_account_id": sub_account_id}, {"_id": 0})) # Excludes the MongoDB _id field from the result
        return QuestionUserResponse(success=True, responses=responses, message="Responses retrieved successfully")

# Retrieves a single response for a given sub_account_id and question_id
def get_question_response(sub_account_id, question_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["QuestionUser"]
        
        responses = list(collection.find({"sub_account_id": sub_account_id, "question_id": question_id}, {"_id": 0})) # Excludes the MongoDB _id field from the result
        if not responses:
            return QuestionUserResponse(success=False, message="Response not found")
        
        return QuestionUserResponse(success=True, responses=responses, message="Response retrieved successfully")
    
def get_question_responses(question_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["QuestionUser"]
        
        responses = list(collection.find({"question_id": question_id}, {"_id": 0})) # Excludes the MongoDB _id field from the result
        return QuestionUserResponse(success=True, responses=responses, message="Responses retrieved successfully")
    
def get_last_20_questions(question_id=None, sub_account_id=None):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["QuestionUser"]
        if question_id != None:
            responses = list(collection.find({"question_id": question_id}, {"_id": 0}).sort("timestamp_utc", -1).limit(20))

        elif sub_account_id != None:
            responses = list(collection.find({"sub_account_id": sub_account_id}, {"_id": 0}).sort("timestamp_utc", -1).limit(20))
        return QuestionUserResponse(success=True, responses=responses, message="Responses retrieved successfully")