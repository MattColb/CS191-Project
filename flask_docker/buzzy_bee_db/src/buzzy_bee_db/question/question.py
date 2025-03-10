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
        database = client.get_default_database()
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
            "difficulty": difficulty,
            "attempts": 0,
            "correct_attempts": 0
        })
        
        return QuestionResponse(success=True, question_id=question_id)

def update_difficulty(question_id, difficulty):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
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
        database = client.get_default_database()
        collection = database["Questions"]
        
        # Check if the question already exists
        query = collection.find({"question_id": question_hash}, {"_id": 0})
        query = query.to_list()
        if len(query) != 1:
            return QuestionResponse(success=False, message="The question doesn't exist or exists more than once")
    
        return QuestionResponse(question=query[0], success=True, message="Got Question")

    
"""
def get_question(question_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Questions"]
        
        # Retrieve the question
        query = collection.find_one({"question_id": question_id}, {"_id": 0})
        if not query:
            return QuestionResponse(success=False, message="The question doesn't exist")

        return QuestionResponse(success=True, question_id=question_id, message="Got Question")
"""

def get_closest_questions(rating, subject):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Questions"]

        query = {
            "category": subject,
            "difficulty": {"$gte": rating - 100, "$lte": rating + 100}
        }
        questions = list(collection.find(query, {"_id": 0}))
        return random.choice(questions) if questions else None
    
# Returns the number of attempts for a given question
def get_question_attempt_count(question_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Questions"]
        question = collection.find_one({"question_id": question_id})
        return question.get("attempts", 0) if question else 0

# Returns the number of correct attempts for a given question
def get_question_correct_count(question_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Questions"]
        question = collection.find_one({"question_id": question_id})
        return question.get("correct_attempts", 0) if question else 0

# Adjusts the attempt count for a question
def adjust_question_attempt_count(question_id, count):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Questions"]
        collection.update_one({"question_id": question_id}, {"$inc": {"attempts": count}}, upsert=True)

# Adjusts the correct attempt count for a question
def adjust_question_correct_count(question_id, count):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        collection = database["Questions"]
        collection.update_one({"question_id": question_id}, {"$inc": {"correct_attempts": count}}, upsert=True)
