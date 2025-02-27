import os
from pymongo import MongoClient
from dotenv import load_dotenv
from uuid import uuid4
from .question_response import QuestionResponse

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

def add_question(question, answer, category, difficulty):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client["buzzy_bee_db"]
        collection = database["Questions"]
        
        # Creating a new question ID
        question_id = str(uuid4())
        
        # Check if the question already exists
        query = collection.find({"question": question})
        if query.count() > 0:
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