from fastapi.testclient import TestClient
from main import app
import os

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

def test_create_and_read_person():
    post_response = client.post(
        "/person/create/", 
        headers={"api-key": API_KEY}, 
        json=person_json
    )
    assert post_response.status_code == 200
    assert post_response.json().get("result") == person_json
    get_response = client.get(
        "/person/read/", 
    )
    assert get_response.status_code == 200
    assert get_response.json().get("result") == person_json