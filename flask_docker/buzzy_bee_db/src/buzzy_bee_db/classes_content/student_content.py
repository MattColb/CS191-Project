import os
from pymongo import MongoClient
from dotenv import load_dotenv
from uuid import uuid4
from .classes_content_response import ClassContentResponse

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

def get_student_classes(sub_account_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Classes"]

        response = list(collection.find({"students":sub_account_id}))

        return ClassContentResponse(success=True, class_information=response)

def get_student_content_db(classes):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Content"]

        response = list(collection.find({"class_id":{"$in":classes}}))

        return ClassContentResponse(success=True, content_information=response)

