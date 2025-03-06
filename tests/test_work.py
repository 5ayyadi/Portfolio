from fastapi.testclient import TestClient
from main import app
import os

os.environ['TESTING'] = '1'
API_KEY = os.getenv("API_KEY")

client = TestClient(app)

work_json = {
    "company": "Example Corp",
    "position": "Software Engineer",
    "start": "2020-01",
    "end": "2023-01",
    "description": "Worked on various software projects."
}

def test_create_work():
    response = client.post(
        "/work/create/", 
        headers={"api-key": API_KEY}, 
        json=work_json
    )
    assert response.status_code == 200
    assert response.json().get("result")[0].get("company") == work_json.get("company")
    assert response.json().get("msg") == "Work experience created successfully"
    work_json["id"] = response.json().get("result")[0].get("id")

def test_read_work():
    response = client.get(
        "/work/read/", 
    )
    assert response.status_code == 200
    assert any(work["company"] == work_json["company"] for work in response.json().get("result"))