# app/checkpoint/mongo_checkpointer.py

from langgraph.checkpoint.mongodb import MongoDBSaver
from app.db.mongo import get_mongo_client

def get_mongo_checkpointer():
    return MongoDBSaver(
        client=get_mongo_client(),
        db_name="ai_hr_assistant",
        collection_name="graph_checkpoints",
    )
