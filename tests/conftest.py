import pytest
import os
from core.db import MongoDBClient
import logging

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    MongoDBClient.initialize(os.getenv('TEST_MONGO_URI'))
    logging.info("MongoDB server is started")
    yield
    db_client = MongoDBClient.get_client()
    db_client.drop_database("Portfolio")
    db_client.close()
    MongoDBClient._instance = None