import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["username"] == "testuser"

def test_register_duplicate_username():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "duplicate",
            "email": "dup1@example.com",
            "password": "testpass123"
        }
    )
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "duplicate",
            "email": "dup2@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 400

def test_login_success():
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "logintest",
            "email": "login@example.com",
            "password": "testpass123"
        }
    )
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "logintest",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401

def test_get_current_user_without_token():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

def test_get_current_user_with_token():
    # Register and login
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "meuser",
            "email": "me@example.com",
            "password": "testpass123"
        }
    )
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "meuser",
            "password": "testpass123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "meuser"

