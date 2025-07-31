import logging
from fastapi import APIRouter, Depends, HTTPException
from models import Education, BaseResponse, EducationResponse
from core.db import MongoDBClient
from core.security import get_current_user
from bson import ObjectId
from controllers.time_calculator import calculate_duration
from errors.error_schema import NoResultFound
router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Education Crud
@router.post("/create/", response_model=EducationResponse)
async def create_education(education: Education, current_user: dict = Depends(get_current_user)):
    """
    This function creates a new education experience.
    Requires JWT authentication.
    """
    logger.info("Creating a new education experience by user: %s", current_user['username'])
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    res = education_collection.insert_one(education.model_dump())
    return {"result": [education], "msg": "Education experience created successfully"}


@router.get("/read/", response_model=EducationResponse)
async def read_education_experiences():
    """ 
    Returns all of education experiences 

    Returns:
        list[education]: list of all education experiences
    """
    logger.info("Reading all education experiences")
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    education_experiences = list(education_collection.find())
    logger.info(f"Found {len(education_experiences)} education experiences")
    return {"result": education_experiences}


@router.put("/update/{id}", response_model=EducationResponse)
async def update_education_experience(id: str, education: Education, current_user: dict = Depends(get_current_user)):
    """
    This function updates an existing education experience.
    Requires JWT authentication.
    """
    logger.info(f"Updating education experience with id: {id} by user: {current_user['username']}")
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    result = education_collection.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": education.model_dump()}
    )

    if result.modified_count == 0:
        logger.warning(f"Education experience with id: {id} not found or nothing to update")
        raise NoResultFound
    
    logger.info(f"Education experience with id: {id} updated successfully")
    return {"result": [education], "msg": "Education experience updated successfully"}


@router.delete("/delete/{id}", response_model=BaseResponse)
async def delete_education_experience(id: str, current_user: dict = Depends(get_current_user)):
    """
    This function deletes an education experience.
    Requires JWT authentication.
    """
    logger.info(f"Deleting education experience with id: {id} by user: {current_user['username']}")
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    result = education_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        logger.warning(f"Failed to delete education with this id : {id} ")
        raise HTTPException(status_code=404, detail="Failed to delete the education experience")

    logger.info(f"Education experience with id: {id} deleted successfully")
    return {"msg": "Education experience deleted successfully"}


@router.get("/duration/", response_model=BaseResponse)
async def calc_duration(id: str | None = None):
    """
        This function calculates the duration of an education experience.
    """
    logger.info(f"Calculating duration for education experience with id: {id}")
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    education_dict = education_collection.find_one(filter={"_id": ObjectId(id)})
    if not education_dict:
        logger.warning(f"Education experience with id: {id} not found")
        raise NoResultFound
    year, month = calculate_duration(start=education_dict.get("start"), end=education_dict.get("end"))
    logger.info(f"Calculated duration: {year} years and {month} months for education experience with id: {id}")
    return {"result": {"duration": {"years": year, "months": month}}}