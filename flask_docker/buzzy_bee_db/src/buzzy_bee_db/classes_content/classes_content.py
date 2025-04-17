import os
from pymongo import MongoClient
from dotenv import load_dotenv
from uuid import uuid4
from .classes_content_response import ClassContentResponse

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

def create_class(teacher_id, class_name):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Classes"]

        class_id = str(uuid4())

        collection.insert_one({
            "teacher_id":teacher_id,
            "class_name":class_name,
            "class_id":class_id,
            "students":[],
            "content_ids":[]
        })

        return ClassContentResponse(success=True, class_id=class_id)

def get_teacher_classes(teacher_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Classes"]

        teacher_classes = list(collection.find({"teacher_id":teacher_id}))

        if teacher_classes != None:
            return ClassContentResponse(success=True, class_information=teacher_classes)
        else:
            return ClassContentResponse(success=True, class_information=[])

def get_class_information(class_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Classes"]

        curr_class = collection.find_one({"class_id":class_id})

        return ClassContentResponse(success=True, class_information=curr_class)
    
def add_students_to_class_db(class_id, students):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Classes"]

        collection.update_one({"class_id":class_id}, {"$addToSet":{"students":{"$each": students}}})

        return ClassContentResponse(success=True, class_id=class_id)
    
def add_class_content(teacher_id, class_id, video_link, due_date, title):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        content = database["Content"]

        content_id = str(uuid4())

        content.insert_one({
            "teacher_id":teacher_id,
            "class_id":class_id,
            "content_id":content_id,
            "video_url":video_link,
            "due_date":due_date,
            "title":title
        })

        classes = database["Classes"]

        classes.update_one({"class_id":class_id}, {"$addToSet":{"content_ids":content_id}})

        return ClassContentResponse(success=True, content_id=content_id)
    
def get_content_information(content_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Content"]

        content_information = collection.find_one({"content_id":content_id})

        return ClassContentResponse(success=True, content_information=content_information)
    
def get_class_content(class_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Content"]

        content_in_class = list(collection.find({"class_id":class_id}))

        if content_in_class != None:
            return ClassContentResponse(success=True, content_information=content_in_class)
        else:
            return ClassContentResponse(success=True, content_information=[])

def remove_students_db(class_id, students):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Classes"]

        collection.update_one({"class_id":class_id}, {"$pull":{"students":{"$in": students}}})

        return ClassContentResponse(success=True, class_id=class_id)