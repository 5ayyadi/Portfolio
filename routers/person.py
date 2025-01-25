import logging
from fastapi import APIRouter, Depends
from models import PersonResponse, Person, BaseResponse
from core.db import MongoDBClient
from core.security import api_key_required
from controllers.time_calculator import calculate_age

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/create/", response_model=PersonResponse, dependencies=[Depends(api_key_required)])
async def create_person(person: Person):
    """
        This Function creates the personal info,
        if there's an exisiting person modify it.
    """
    logger.info(f"Creating or updating person {person.model_dump_json()}")
    person_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Person")
    existing_person = person_collection.find_one()
    
    if existing_person is not None:
        logger.info("Existing person found, updating")
        person_collection.update_one(
            filter={"_id": existing_person.get("_id")},
            update={"$set": person.model_dump()}
        )
        logger.info("Person updated successfully")
        return {"result": person, "msg": "Person updated successfully"}
    else:
        logger.info("No existing person found, creating new person")
        # Insert a new person document if none exists
        res = person_collection.insert_one(person.model_dump())
        logger.info("Person created successfully")
        return {"result": person, "msg": "Person created successfully"}


@router.get("/read/", response_model=PersonResponse)
async def read_person():
    logger.info("Reading person information")
    person_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Person")
    person = person_collection.find_one()
    logger.info("Person information retrieved")
    return {"result": person}

@router.get("/age/", response_model=BaseResponse)
async def calc_age():
    logger.info("Calculating age")
    person_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Person")
    person_dict = person_collection.find_one()
    person = Person(**person_dict)
    age = calculate_age(person)
    logger.info(f"Age calculated: {age}")
    return {"result": {"age": age}}