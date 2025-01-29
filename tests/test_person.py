from fastapi.testclient import TestClient
from main import app
import os 
import logging

os.environ['TESTING'] = '1'
API_KEY = os.getenv("API_KEY")

client = TestClient(app)

person_json = {
    "name": "John Doe",
    "birthday": "2002-02-02",
    "position": "Worker",
    "contact": {
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "linkedin": "https://www.linkedin.com/in/johndoe",
        "github": "https://www.github.com/johndoe"
    },
    "description": "A hardworking individual."
}

def test_create_person():
    
    response = client.post(
        "/person/create", 
        headers={"api-key": API_KEY}, 
        json=person_json)
    
    assert response.status_code == 200
    assert response.json().get("result") == person_json
    assert response.json().get("msg") == "Person created successfully"
    print(response.json())


def test_create_person_bad_token():
    response = client.post(
        "/person/create",
        headers={"api-key": "bad_token"},
        json=person_json,
    )
    assert response.status_code == 403
    assert response.json().get("detail") == "Could not validate credentials"


def test_create_existing_person():
    person_json["name"] = "Jane Doe"
    response = client.post(
        "/person/create",
        headers={"api-key": API_KEY},
        json=person_json,
    )
    assert response.status_code == 200
    assert response.json().get("msg") == "Person updated successfully"

def test_read_person():
    response = client.get(
        "/person/read", 
    )
    assert response.status_code == 200
    assert response.json().get("result") == person_json
