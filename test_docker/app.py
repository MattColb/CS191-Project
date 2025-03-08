from flask import Flask, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)

# Fetch the MongoDB connection string from the environment
mongodb_conn_string = os.getenv("MONGODB_CONN_STRING")

# Connect to MongoDB
client = MongoClient(mongodb_conn_string)
db = client.get_database()  # Use the default database in the connection string

@app.route('/')
def index():
    try:
        # Fetch the list of collections in the database to test the connection
        collections = db.list_collection_names()
        return jsonify({"collections": collections}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
