# database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))  # Should be 'mongodb://localhost:27017'

db = client["chatbot"]  # Database name
users_collection = db["users"]  # Collection name

def add_user(username, password):
    print(f"Adding user: {username}")
    if users_collection.find_one({"username": username}):
        print("User already exists.")
        return False
    users_collection.insert_one({"username": username, "password": password})
    print("User added successfully.")
    return True
def verify_user(username, password):
    user = users_collection.find_one({"username": username, "password": password})
    return user is not None

