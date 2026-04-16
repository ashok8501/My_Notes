import os
from pymongo import MongoClient

# Get MongoDB URL from environment variable
MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

db = client["student_notes_app"]

notes_collection = db["notes"]
users_collection = db["users"]