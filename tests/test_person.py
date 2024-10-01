from fastapi.testclient import TestClient
from .mongodb_test import mongodb_test
from main import app
import os

client = TestClient(app)

API_KEY = os.getenv("API_KEY")


@mongodb_test(collection="Person")
def test_create_person():
    person = {
        "name": "John Doe", 
        "birthday": "1999-09-09", 
        "position": "Software Developer", 
        "contact": {
            "email": "john@example.com",
            "phone": "1234567890"
        },
        "description": "An experienced software developer."
    }
    
    response = client.post(
        "/person/create",
        headers={"api-key": API_KEY},  
        json=person,
    )
    
    assert response.status_code == 200
    assert response.json() == {
        "msg": "Person updated successfully",
        "status_code": 200,
        "result": {
            "name": "John Doe",
            "birthday": "1999-09-09",
            "position": "Software Developer",
            "contact": {
                "email": "john@example.com",
                "phone": "1234567890",
                "linkedin": None  # Added this key
            },
            "description": "An experienced software developer."
        }
    }
    
@mongodb_test(collection="Person")
def test_read_person():
    response = client.get("/person/read")
    assert response.status_code == 200
    assert response.json() == {
        "msg": "OK",
        "status_code": 200,
        "result": {
            "name": "John Doe",
            "birthday": "1999-09-09",
            "position": "Software Developer",
            "contact": {
                "email": "john@example.com",
                "phone": "1234567890",
                "linkedin": None  # Added this key
            },
            "description": "An experienced software developer."
        }
    }