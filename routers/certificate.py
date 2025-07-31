from fastapi import APIRouter, Depends, HTTPException
from models import Certificate, BaseResponse, CertificateResponse
from core.db import MongoDBClient
from core.security import get_current_user
import logging
from bson import ObjectId
from errors.error_schema import NoResultFound

router = APIRouter()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Certificate Crud
@router.post("/create/", response_model=CertificateResponse)
async def create_certificate(certificate: Certificate, current_user: dict = Depends(get_current_user)):
    """
        This Function creates a certificate info,
        adds it to Certificate collection.
        Requires JWT authentication.
    """
    
    certificate_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Certificate")
    res = certificate_collection.insert_one(certificate.model_dump())
    logging.info(f"Certificate created with id: {res.inserted_id} by user: {current_user['username']}")
    return {"result": [certificate], "msg": "Certificate created successfully"}


@router.get("/read/",response_model=CertificateResponse)
async def read_certificate_experiences():
    """ 
        returns all of certificate experiences 

    Returns:
        list[certificate]: list of all certificate experiences
    """
    certificate_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Certificate")
    certificate_experiences = list(certificate_collection.find())
    if len(certificate_experiences) == 0:
        raise NoResultFound        
    return {"result": certificate_experiences}

@router.put("/update/{id}", response_model=CertificateResponse)
async def update_certificate(id: str, certificate: Certificate, current_user: dict = Depends(get_current_user)):
    """
        This Function updates a certificate info by its ID,
        modifies it in the Certificate collection.
        Requires JWT authentication.
    """
    certificate_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Certificate")

    update_data = certificate.model_dump(exclude_unset=True)  

    result = certificate_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    
    if result.matched_count == 0:
        raise NoResultFound

    logging.info(f"Certificate updated with id: {id} by user: {current_user['username']}")
    
    updated_certificate = certificate_collection.find_one({"_id": ObjectId(id)})
    return {"result": [updated_certificate], "msg": "Certificate updated successfully"}

@router.delete("/delete/{id}", response_model=BaseResponse)
async def delete_certificate(id: str, current_user: dict = Depends(get_current_user)):
    """
        This Function deletes a certificate by its ID,
        removes it from the Certificate collection.
        Requires JWT authentication.
    """
    certificate_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Certificate")
    
    # Retrieve the document before deleting
    certificate_doc = certificate_collection.find_one({"_id": ObjectId(id)})
    
    if certificate_doc is None:
        raise NoResultFound
    
    # Perform the deletion
    result = certificate_collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Failed to delete the certificate")
    
    logging.info(f"Certificate deleted with id: {id} by user: {current_user['username']}")

    certificate_doc["_id"] = str(certificate_doc["_id"])
    return {"result": certificate_doc, "msg": "Certificate deleted successfully"}

