import os
from pymongo import MongoClient
from dotenv import load_dotenv
from uuid import uuid4
from .question_response import QuestionResponse
import random

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

def add_question(question_id, question, answer, category, difficulty):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Questions"]
        
        # Check if the question already exists
        query = collection.find({"question_id": question_id})
        if len(query.to_list()) > 0:
            return QuestionResponse(success=False, message="This question already exists")

        # Insert the question into the database
        response = collection.insert_one({
            "question_id": question_id,
            "question": question,
            "answer": answer,
            "category": category,
            "difficulty": difficulty
        })
        
        return QuestionResponse(success=True, question_id=question_id)

def update_difficulty(question_id, difficulty):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Questions"]
        
        # Update the difficulty of the question
        result = collection.update_one(
            {"question_id": question_id},
            {"$set": {"difficulty": difficulty}}
        )
        
        if result.matched_count == 0:
            return QuestionResponse(success=False, message="Question not found")
       
        return QuestionResponse(success=True, message="Difficulty updated")

def get_question(question_hash):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Questions"]
        
        # Check if the question already exists
        query = collection.find({"question_id": question_hash}, {"_id": 0})
        query = query.to_list()
        if len(query) != 1:
            return QuestionResponse(success=False, message="The Question Doesn't Exist or exists more than once")
    
        return QuestionResponse(question_id=query[0], success=True, message="Got Question")

def get_closest_questions(rating, subject):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Questions"]

        query = {
            "category": subject,
            "difficulty": {"$gte": rating - 100, "$lte": rating + 100}
        }
        questions = list(collection.find(query, {"_id": 0}))
        return random.choice(questions)
