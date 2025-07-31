import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_login_with_valid_credentials():
    """Test login with valid credentials"""
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "access_token" in data["result"]
    assert data["result"]["token_type"] == "bearer"
    assert "expires_in" in data["result"]

def get_valid_token():
    """Helper function to get a valid token"""
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    return response.json()["result"]["access_token"]

def test_login_with_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]

def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without token"""
    response = client.get("/auth/protected")
    assert response.status_code == 403  # Should be unauthorized

def test_protected_endpoint_with_valid_token():
    """Test accessing protected endpoint with valid token"""
    # First, get a token
    token = get_valid_token()
    
    # Then use it to access protected endpoint
    response = client.get(
        "/auth/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "admin" in data["result"]["message"]

def test_protected_endpoint_with_invalid_token():
    """Test accessing protected endpoint with invalid token"""
    response = client.get(
        "/auth/protected",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401

def test_me_endpoint_with_valid_token():
    """Test getting user info with valid token"""
    # First, get a token
    token = get_valid_token()
    
    # Then use it to access user info
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"]["username"] == "admin"
    assert data["result"]["is_active"] == True

def test_create_person_with_jwt_token():
    """Test creating person with JWT authentication"""
    # First, get a token
    token = get_valid_token()
    
    # Test data that matches the Person model structure
    person_data = {
        "name": "John Doe",
        "birthday": "1990-01-01",
        "position": "Software Engineer",
        "contact": {
            "email": "john@example.com",
            "phone": "+1234567890",
            "linkedin": "https://www.linkedin.com/in/johndoe",
            "github": "https://github.com/johndoe"
        },
        "description": "Experienced software engineer"
    }
    
    # Create person with JWT token
    response = client.post(
        "/person/create/",
        json=person_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"]["name"] == "John Doe"

def test_create_person_without_token():
    """Test creating person without JWT token should fail"""
    person_data = {
        "name": "John Doe",
        "birthday": "1990-01-01",
        "position": "Software Engineer",
        "contact": {
            "email": "john@example.com",
            "phone": "+1234567890",
            "linkedin": "https://www.linkedin.com/in/johndoe",
            "github": "https://github.com/johndoe"
        },
        "description": "Experienced software engineer"
    }
    
    response = client.post(
        "/person/create/",
        json=person_data
    )
    assert response.status_code == 403  # Should be unauthorized
