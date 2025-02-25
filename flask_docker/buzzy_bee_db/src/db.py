import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import certifi

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI from the environment
uri = os.getenv("MONGO_URI")

if not uri:
    raise ValueError("MongoDB URI is not set. Make sure to add it to your .env file.")

# Connect to MongoDB using the certifi bundle
client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))
db = client["Test-Database0"]

# Test connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB.")
except Exception as e:
    print("Failed to connect to MongoDB:", e)


