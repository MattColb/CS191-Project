from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)

@app.route("/")
def home():
    client = MongoClient(os.environ["MONGO_URI"])

    client.admin.command("ping")
    print("Successful")
    client.close()
    return "Hello from Docker"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
