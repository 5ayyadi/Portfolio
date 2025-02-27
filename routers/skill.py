import logging
from fastapi import APIRouter, Depends, HTTPException
from models import Skill, SkillResponse, BaseResponse
from core.db import MongoDBClient
from core.security import api_key_required
from bson import ObjectId
from errors.error_schema import NoResultFound

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/create/", response_model=SkillResponse, dependencies=[Depends(api_key_required)])
async def create_skill(skill: Skill):
    """creates the skill with corresponding level

    Args:
        skill (Skill): A skill with a name and level from 1 to 6
    """
    logger.info("Creating a new skill: %s", skill)
    skill_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Skill")
    res = skill_collection.insert_one(skill.model_dump())
    logger.info("Skill created successfully with id: %s", res.inserted_id)
    return {"result": [skill], "msg": "Skill created successfully"}


@router.get("/read/", response_model=SkillResponse)
async def read_skills():
    """ 
        returns all of skills

    Returns:
        list[skill]: list of all skills
    """
    logger.info("Reading all skills")
    skill_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Skill")
    skills = list(skill_collection.find())
    logger.info("Found %d skills", len(skills))
    return {"result": skills}


@router.put("/update/{id}", response_model=SkillResponse, dependencies=[Depends(api_key_required)])
async def update_skill(id: str, skill: Skill):
    """
        This Function updates a skill by ID.
    """
    logger.info("Updating skill with id: %s", id)
    skill_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Skill")
    updated_skill = skill_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": skill.model_dump()},
        return_document=True
    )
    if updated_skill is None:
        logger.error("Skill with id %s not found", id)
        raise NoResultFound
    
    logger.info("Skill with id %s updated successfully", id)
    return {"result": [updated_skill], "msg": "Skill updated successfully"}


@router.delete("/delete/{id}", response_model=BaseResponse, dependencies=[Depends(api_key_required)])
async def delete_skill(id: str):
    """
        This Function deletes a skill by its ID. 
    """
    logger.info("Deleting skill with id: %s", id)
    skill_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Skill")
    delete_result = skill_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        logger.error("Skill with id %s not found", id)
        raise NoResultFound
    
    logger.info("Skill with id %s deleted successfully", id)
    return {"msg": "Skill deleted successfully"}