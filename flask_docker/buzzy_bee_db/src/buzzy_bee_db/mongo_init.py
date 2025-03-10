from dotenv import load_dotenv
from pymongo import MongoClient
import os
from pprint import pprint

curr_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(curr_dir, "../../../.env"))

def create_cols():
    conn_string = os.getenv("MONGODB_CONN_STRING")
    client = MongoClient(conn_string)
    database = client.get_default_database()
    collections_to_create = ["Users"]
    for collection in collections_to_create:
        if collection in database.list_collection_names():
            continue
        else:
            database.create_collection(collection)
