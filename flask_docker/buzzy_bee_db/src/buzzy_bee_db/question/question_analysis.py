import os
from pymongo import MongoClient
from dotenv import load_dotenv

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../../.env"))

# Needs to be adjusted !!!

def analyze_question_difficulty(question_id):
    connection = os.getenv("MONGODB_CONN_STRING")
    with MongoClient(connection) as client:
        database = client.get_default_database()
        question_collection = database["Questions"]
        response_collection = database["QuestionUser"]

        # Get question info
        question = question_collection.find_one({"question_id": question_id})
        if not question:
            return {"error": "Question not found"}

        # Get all responses for the question
        responses = list(response_collection.find({"question_id": question_id}))

        if not responses:
            return {"message": "No responses for this question"}

        total_attempts = len(responses)
        correct_attempts = sum(1 for r in responses if r.get("answered_correctly", False))
        success_rate = correct_attempts / total_attempts if total_attempts > 0 else 0

        # Update difficulty based on success rate
        if success_rate < 0.3:
            new_difficulty = min(question["difficulty"] + 1, 1000)  # Harder
        elif success_rate > 0.7:
            new_difficulty = max(question["difficulty"] - 1, 0)  # Easier
        else:
            new_difficulty = question["difficulty"]  # No change

        question_collection.update_one({"question_id": question_id}, {"$set": {"difficulty": new_difficulty}})
        
        return {"success": True, "new_difficulty": new_difficulty}
