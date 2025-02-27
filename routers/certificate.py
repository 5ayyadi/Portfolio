from fastapi import APIRouter, Depends, HTTPException
from models import Certificate, BaseResponse, CertificateResponse
from core.db import MongoDBClient
from core.security import api_key_required
import logging
from bson import ObjectId
from errors.error_schema import NoResultFound

router = APIRouter()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Certificate Crud
@router.post("/create/", response_model=CertificateResponse, dependencies=[Depends(api_key_required)])
async def create_certificate(certificate: Certificate):
    """
        This Function creates a certificate info,
        adds it to Certificate collection
    """
    
    certificate_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Certificate")
    res = certificate_collection.insert_one(certificate.model_dump())
    logging.info(f"Certificate created with id: {res.inserted_id}")
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

@router.put("/update/{id}", response_model=CertificateResponse, dependencies=[Depends(api_key_required)])
async def update_certificate(id: str, certificate: Certificate):
    """
        This Function updates a certificate info by its ID,
        modifies it in the Certificate collection
    """
    certificate_collection = MongoDBClient.get_client().get_database("Portfolio").get_collection("Certificate")

    update_data = certificate.model_dump(exclude_unset=True)  

    result = certificate_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    
    if result.matched_count == 0:
        raise NoResultFound

    logging.info(f"Certificate updated with id: {id}")
    
    updated_certificate = certificate_collection.find_one({"_id": ObjectId(id)})
    return {"result": [updated_certificate], "msg": "Certificate updated successfully"}

@router.delete("/delete/{id}", response_model=BaseResponse, dependencies=[Depends(api_key_required)])
async def delete_certificate(id: str):
    """
        This Function deletes a certificate by its ID,
        removes it from the Certificate collection
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
    
    logging.info(f"Certificate deleted with id: {id}")

    certificate_doc["_id"] = str(certificate_doc["_id"])
    return {"result": certificate_doc, "msg": "Certificate deleted successfully"}

