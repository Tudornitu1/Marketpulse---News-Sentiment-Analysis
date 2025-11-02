from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv
load_dotenv()


def get_db():
    MONGODB_URI = os.getenv("MONGODB_URI")
    client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
    db = client['marketpulse_db']
    return db

if __name__ == "__main__":
    db = get_db()
    print("Database connection successful.")