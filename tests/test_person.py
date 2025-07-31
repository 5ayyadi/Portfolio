from fastapi.testclient import TestClient
from main import app
from tests.auth_helper import get_auth_headers
import os

os.environ['TESTING'] = '1'

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

def test_create_and_read_person():
    post_response = client.post(
        "/person/create/", 
        headers=get_auth_headers(), 
        json=person_json
    )
    assert post_response.status_code == 200
    assert post_response.json().get("result") == person_json
    get_response = client.get(
        "/person/read/", 
    )
    assert get_response.status_code == 200
    assert get_response.json().get("result") == person_json