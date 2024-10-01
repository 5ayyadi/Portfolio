import functools
from core.db import MongoDBClient

def mongodb_test(uri: str = "mongodb://localhost:27017/", db_name: str = "Test", collection: str = None):
    def decorator_mongodb_test(func):
        @functools.wraps(func)
        def wrapper_mongodb_test(*args, **kwargs):
            # Initialize MongoDB
            MongoDBClient.initialize(uri)
            print("MongoDB client initialized for testing.")

            try:
                return func(*args, **kwargs)
            finally:
                db = MongoDBClient.get_client().get_database(db_name)
                db.drop_collection(collection)
                print(f"MongoDB test teardown complete for collection: {collection}.")
                
        return wrapper_mongodb_test
    return decorator_mongodb_test
