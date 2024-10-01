from fastapi import FastAPI
from routers import person, work_experience, certificate, education, skill
from core.db import MongoDBClient
from contextlib import asynccontextmanager
import os 
import logging

MONGO_URI = os.getenv("MONGO_URI")  or "mongodb://localhost:27017" 

@asynccontextmanager
async def lifespan(app: FastAPI):
    uri = MONGO_URI
    is_mongo_started = MongoDBClient.initialize(uri)
    if is_mongo_started is True:
        logging.info("MongoDB server is started")
    db_client = MongoDBClient.get_client()
    yield
    
    db_client.close()
    MongoDBClient._instance = None

app = FastAPI(lifespan=lifespan)

app.include_router(person.router, prefix="/person",tags=["Person"])
app.include_router(work_experience.router, prefix="/work",tags=["Work"])
app.include_router(education.router, prefix="/education",tags=["Education"])
app.include_router(certificate.router, prefix="/certificate",tags=["Certificate"])
app.include_router(skill.router, prefix="/skill", tags=["Skill"])
