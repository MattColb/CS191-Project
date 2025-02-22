from dotenv import load_dotenv
from pymongo import MongoClient
import os
from pprint import pprint

load_dotenv()

def create_cols():
    conn_string = os.getenv("MONGODB_CONN_STRING")
    client = MongoClient(conn_string)
    if "buzzy_bee_db"
    if "Users" in my_db.list_collection_names():
        return
    else:
        users = my_db["Users"]

if __name__ == "__main__":
    pprint(create_cols())