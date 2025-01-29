from fastapi.testclient import TestClient
from main import app
import os 

os.environ['TESTING'] = '1'
API_KEY = os.getenv("API_KEY")

client = TestClient(app)

education_json = {
    "institution": "University of Example",
    "degree": "Bachelor of Science",
    "start": "2018-09",
    "end": "2022-06",
    "desc": "Studied various aspects of computer science."
}

def test_create_education():
    response = client.post(
        "/education/create/", 
        headers={"api-key": API_KEY}, 
        json=education_json
    )
    
    assert response.status_code == 200
    assert response.json().get("result")[0].get("institution") == education_json.get("institution")
    assert response.json().get("msg") == "Education experience created successfully"
    education_json["id"] = response.json().get("result")[0].get("id")


def test_read_education():
    response = client.get(
        "/education/read/", 
    )
    assert response.status_code == 200
    assert any(edu["institution"] == education_json["institution"] for edu in response.json().get("result"))


def test_duration_education():
    response = client.get(
        f"/education/duration/{education_json['id']}",
    )
    assert response.status_code == 200
    duration = response.json().get("result").get("duration")
    assert duration["years"] == 3
    assert duration["months"] == 9


def test_create_education_bad_token():
    response = client.post(
        "/education/create/",
        headers={"api-key": "bad_token"},
        json=education_json,
    )
    assert response.status_code == 403
    assert response.json().get("detail") == "Could not validate credentials"


def test_update_education():
    updated_education_json = education_json.copy()
    updated_education_json["degree"] = "Master of Science"
    
    response = client.put(
        "/education/update/",
        headers={"api-key": API_KEY},
        json=updated_education_json,
    )
    assert response.status_code == 200
    assert response.json().get("msg") == "Education experience updated successfully"
    assert response.json().get("result")[0]["degree"] == "Master of Science"


def test_delete_education():
    response = client.delete(
        "/education/delete/",
        headers={"api-key": API_KEY},
        json={"id": education_json["id"]},
    )
    assert response.status_code == 200
    assert response.json().get("msg") == "Education experience deleted successfully"
