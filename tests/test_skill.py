from fastapi.testclient import TestClient
from main import app
from tests.auth_helper import get_auth_headers
import os

os.environ['TESTING'] = '1'

client = TestClient(app)

skill_json = {
    "name": "Python",
    "level": 5,
    "tag": "Language"
}

def test_create_and_read_skill():
    response = client.post(
        "/skill/create/", 
        headers=get_auth_headers(), 
        json=skill_json
    )
    print(response.json())  # Add this line to print the response content
    assert response.status_code == 200
    assert response.json().get("result")[0].get("name") == skill_json.get("name")
    skill_json["id"] = response.json().get("result")[0].get("id")

    response = client.get(
        "/skill/read/", 
    )
    assert response.status_code == 200
    assert any(skill["name"] == skill_json["name"] for skill in response.json().get("result"))