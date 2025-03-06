from fastapi.testclient import TestClient
from main import app
import os

os.environ['TESTING'] = '1'
API_KEY = os.getenv("API_KEY")

client = TestClient(app)

certificate_json = {
    "name": "Certified Kubernetes Administrator",
    "date": "2023-05",
    "desc": "Certification for Kubernetes administration."
}

def test_create_certificate():
    response = client.post(
        "/certificate/create/", 
        headers={"api-key": API_KEY}, 
        json=certificate_json
    )
    assert response.status_code == 200
    assert response.json().get("result")[0].get("name") == certificate_json.get("name")
    assert response.json().get("msg") == "Certificate created successfully"
    certificate_json["id"] = response.json().get("result")[0].get("id")

def test_read_certificate():
    response = client.get(
        "/certificate/read/", 
    )
    assert response.status_code == 200
    assert any(cert["name"] == certificate_json["name"] for cert in response.json().get("result"))