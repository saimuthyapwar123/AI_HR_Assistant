from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://saiprasad:IeRjrY04NFZwXR4I@newarticles.waa3uh5.mongodb.net/")
DB_NAME = os.getenv("MONGO_DB_NAME", "ai_hr_assistant")

_client: MongoClient | None = None


def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        if not MONGO_URI:
            raise RuntimeError("❌ MONGO_URI not set")
        _client = MongoClient(MONGO_URI)
    return _client


def get_database() -> Database:
    return get_mongo_client()[DB_NAME]


def get_collection(name: str) -> Collection:
    return get_database()[name]
