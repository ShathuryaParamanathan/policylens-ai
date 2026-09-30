from pymongo import MongoClient
from .config import settings


client = MongoClient(settings.mongodb_uri)

db = client[settings.mongodb_db]


def check_database_connection():
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        print("MongoDB connection error:", e)
        return False