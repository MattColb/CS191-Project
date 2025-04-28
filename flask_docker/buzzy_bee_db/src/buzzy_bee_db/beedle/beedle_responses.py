import os
from pymongo import MongoClient
from dotenv import load_dotenv
from .beedle_responses_response import BeedleResponsesResponse

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

{
    "date":"2024-20-2",
    "subaccount_id":"asdf",
    "questions":[
        {
            "question_id":"asdf",
            "answered_correctly":True
        }
    ]
}

def get_beedle_results(subaccount_id, date):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Beedle_Responses"]

        resp = collection.find_one({"date":date, "subaccount_id":subaccount_id})
        
        if resp == None:
            create_beedle_result(subaccount_id, date)
            resp = collection.find_one({"date":date, "subaccount_id":subaccount_id})

        if len(resp.get("questions")) != 5:
            return BeedleResponsesResponse(questions=resp.get("questions"), success=False, message="The user hasn't answered all of the questions")
        
        return BeedleResponsesResponse(questions=resp.get("questions"), success=True)

def add_beedle_question_response(subaccount_id, date, question_id, response):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Beedle_Responses"]

        resp = collection.find_one_and_update({"date":date, "subaccount_id":subaccount_id}, 
                                              {"$push":{"questions":{"question_id":question_id, 
                                                                     "answered_correctly":response}}})
        
        if not resp:
            create_beedle_result(subaccount_id, date)
            resp = collection.find_one_and_update({"date":date, "subaccount_id":subaccount_id}, 
                                              {"$push":{"questions":{"question_id":question_id, 
                                                                     "answered_correctly":response}}})
        
        return BeedleResponsesResponse(success=True)

def create_beedle_result(subaccount_id, date):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Beedle_Responses"]

        if collection.find_one({"date":date, "subaccount_id":subaccount_id}):
            return BeedleResponsesResponse(success=False, message="The user already exists")
        
        collection.insert_one({"date":date, "subaccount_id":subaccount_id, "questions":[]})

        return BeedleResponsesResponse(success=True)