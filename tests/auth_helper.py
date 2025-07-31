from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_auth_token():
    """Helper function to get a valid JWT token for testing"""
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    if response.status_code == 200:
        return response.json()["result"]["access_token"]
    return None

def get_auth_headers():
    """Helper function to get Authorization headers for testing"""
    token = get_auth_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}
