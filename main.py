from fastapi import FastAPI
from routers import person, work_experience, certificate, education, skill, auth
from core.db import MongoDBClient
from core.security import init_default_users
from contextlib import asynccontextmanager
from errors.error_handler import add_default_handlers
import os 
import logging
MONGO_URI = os.getenv('MONGO_URI')
TEST_MONGO_URI = os.getenv('TEST_MONGO_URI')

@asynccontextmanager
async def lifespan(app: FastAPI):
    uri = TEST_MONGO_URI if os.getenv('TESTING') else MONGO_URI
    is_mongo_started = MongoDBClient.initialize(uri)
    if is_mongo_started is True:
        logging.info(f"MongoDB server is started")
        # Initialize default users after DB connection
        if not os.getenv('TESTING'):  # Don't create users during testing
            init_default_users()
    db_client = MongoDBClient.get_client()
    yield
    
    db_client.close()
    MongoDBClient._instance = None

app = FastAPI(lifespan=lifespan)

add_default_handlers(app)

# Auth routes (no prefix for login to be accessible)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(person.router, prefix="/person",tags=["Person"])
app.include_router(work_experience.router, prefix="/work",tags=["Work"])
app.include_router(education.router, prefix="/education",tags=["Education"])
app.include_router(certificate.router, prefix="/certificate",tags=["Certificate"])
app.include_router(skill.router, prefix="/skill", tags=["Skill"])
