from pymongo import MongoClient
from threading import Lock
import logging


class MongoDBClient:
    _instance = None
    _lock = Lock()

    
    @classmethod
    def initialize(cls, mongo_url: str) -> bool:
        with cls._lock:
            if cls._instance is None:
                cls._instance = MongoClient(mongo_url)
        return True

    @classmethod
    def get_client(cls) -> MongoClient:
        if cls._instance is None:
            raise ValueError("MongoDBClient has not been initialized. Call `initialize` first.")
        return cls._instance
