import logging
from fastapi import APIRouter, Depends, HTTPException
from models import Education, BaseResponse, EducationResponse
from core.db import MongoDBClient
from core.security import api_key_required
from bson import ObjectId
from controllers.time_calculator import calculate_duration

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Education Crud
@router.post("/create/", response_model=EducationResponse, dependencies=[Depends(api_key_required)])
async def create_education(education: Education):
    """
    This function creates a new education experience.
    """
    logger.info("Creating a new education experience")
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    res = education_collection.insert_one(education.model_dump())
    logger.info(f"Education experience created with id: {res.inserted_id}")
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


@router.put("/update/{id}", response_model=EducationResponse, dependencies=[Depends(api_key_required)])
async def update_education_experience(id: str, education: Education):
    """
    This function updates an existing education experience.
    """
    logger.info(f"Updating education experience with id: {id}")
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    result = education_collection.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": education.model_dump()}
    )

    if result.modified_count == 0:
        logger.warning(f"Education experience with id: {id} not found or nothing to update")
        raise HTTPException(status_code=404, detail="Education experience not found or nothing to update")
    
    logger.info(f"Education experience with id: {id} updated successfully")
    return {"result": [education], "msg": "Education experience updated successfully"}


@router.delete("/delete/{id}", response_model=BaseResponse, dependencies=[Depends(api_key_required)])
async def delete_education_experience(id: str):
    """
    This function deletes an education experience.
    """
    logger.info(f"Deleting education experience with id: {id}")
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    result = education_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        logger.warning(f"Education experience with id: {id} not found")
        raise HTTPException(status_code=404, detail="Education experience not found")

    logger.info(f"Education experience with id: {id} deleted successfully")
    return {"msg": "Education experience deleted successfully"}


@router.get("/duration/", response_model=BaseResponse)
async def calc_duration(id: str):
    """
        This function calculates the duration of an education experience.
    """
    logger.info(f"Calculating duration for education experience with id: {id}")
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    education_dict = education_collection.find_one(filter={"_id": ObjectId(id)})
    if not education_dict:
        logger.warning(f"Education experience with id: {id} not found")
        raise HTTPException(status_code=404, detail="Education experience not found")
    year, month = calculate_duration(start=education_dict.get("start"), end=education_dict.get("end"))
    logger.info(f"Calculated duration: {year} years and {month} months for education experience with id: {id}")
    return {"result": {"duration": {"years": year, "months": month}}}