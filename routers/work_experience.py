from fastapi import APIRouter, Depends, HTTPException
from models import Work, BaseResponse, WorkResponse
from core.db import MongoDBClient
from core.security import api_key_required
from bson import ObjectId
from controllers.time_calculator import calculate_duration

router = APIRouter()

@router.post("/create", response_model=WorkResponse, dependencies=[Depends(api_key_required)])
async def create_work_experience(work: Work):
    """
        This Function creates the work experience info,
        adds it to Work collection
    """
    
    work_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Work")
    res = work_collection.insert_one(work.model_dump())
    return {"result": [work], "msg": "Work experience created successfully"}


@router.get("/read",response_model=WorkResponse)
async def read_work_experiences():
    """ 
        returns all of work experiences 

    Returns:
        list[work]: list of all work experiences
    """
    work_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Work")
    work_experiences = list(work_collection.find())
    return {"result": work_experiences}


@router.put("/update/{id}", response_model=WorkResponse, dependencies=[Depends(api_key_required)])
async def update_work_experience(id: str, work: Work):
    """
        This Function updates a work experience info by its ID.
    """
    work_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Work")
    updated_work = work_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": work.model_dump()},
        return_document=True
    )

    if updated_work is None:
        raise HTTPException(status_code=404, detail="Work experience not found")
    
    return {"result": [updated_work], "msg": "Work experience updated successfully"}


@router.delete("/delete/{id}", response_model=BaseResponse, dependencies=[Depends(api_key_required)])
async def delete_work_experience(id: str):
    """
        This Function deletes a work experience by its ID.
    """
    work_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Work")
    delete_result = work_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Work experience not found")
    
    return {"msg": "Work experience deleted successfully"}

@router.get("/duration", response_model=BaseResponse)
async def calc_duration(id: str):
    work_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Work")
    work_dict = work_collection.find_one(filter={"_id": ObjectId(id)})
    duration = calculate_duration(start = work_dict.get("start"), end = work_dict.get("end"))
    return {"result":{"duration":duration}}