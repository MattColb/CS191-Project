import os
from pymongo import MongoClient
from dotenv import load_dotenv
from .beedle_questions_response import BeedleQuestionResponse

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

def add_questions(day, question_ids):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Beedle_Questions"]

        collection.insert_one({"date":day, "questions":question_ids})

        return BeedleQuestionResponse(success=True)

def get_questions(day):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Beedle_Questions"]

        response = collection.find_one({"date":day})

        if not response:
            return BeedleQuestionResponse(success=False, message="The date doesn't exist")

        questions = response.get("questions")

        return BeedleQuestionResponse(success=True, questions=questions)