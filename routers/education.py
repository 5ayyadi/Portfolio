from fastapi import APIRouter, Depends, HTTPException
from models import Education, BaseResponse, EducationResponse
from core.db import MongoDBClient
from core.security import api_key_required
from bson import ObjectId
from controllers.time_calculator import calculate_duration

router = APIRouter()


# Education Crud
@router.post("/create/", response_model=EducationResponse, dependencies=[Depends(api_key_required)])
async def create_education(education: Education):
    """
        This Function creates a education experience info,
        adds it to Education collection
    """
    
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    res = education_collection.insert_one(education.model_dump())
    return {"result": [education], "msg": "Education experience created successfully"}


@router.get("/read/",response_model=EducationResponse)
async def read_education_experiences():
    """ 
        returns all of education experiences 

    Returns:
        list[education]: list of all education experiences
    """
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    education_experiences = list(education_collection.find())
    return {"result": education_experiences}

@router.put("/update/{id}", response_model=EducationResponse, dependencies=[Depends(api_key_required)])
async def update_education_experience(id: str, education: Education):
    """
    This function updates an existing education experience.
    """
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    result = education_collection.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": education.model_dump()}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Education experience not found or nothing to update")
    
    return {"result": [education], "msg": "Education experience updated successfully"}


@router.delete("/delete/{id}", response_model=BaseResponse, dependencies=[Depends(api_key_required)])
async def delete_education_experience(id: str):
    """
    This function deletes an education experience.
    """
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    result = education_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Education experience not found")

    return {"msg": "Education experience deleted successfully"}


@router.get("/duration/", response_model=BaseResponse)
async def calc_duration(id: str):
    education_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Education")
    education_dict = education_collection.find_one(filter={"_id": ObjectId(id)})
    duration = calculate_duration(start = education_dict.get("start"), end = education_dict.get("end"))
    return {"result":{"duration":duration}}