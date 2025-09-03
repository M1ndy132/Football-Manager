"""
Integration tests for authentication endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.database.models import User
from app.core.security import get_password_hash


class TestAuthEndpoints:
    """Test authentication-related endpoints."""
    
    def test_user_registration(self, client, test_db):
        """Test user registration endpoint via /api/v1/users/."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "password123"
        }
        
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        
        response_data = response.json()
        assert response_data["username"] == "newuser"
        assert response_data["email"] == "newuser@example.com"
        assert response_data["full_name"] == "New User"
        assert "id" in response_data
        assert "password" not in response_data
    
    def test_user_registration_duplicate_username(self, client, test_db):
        """Test user registration with duplicate username."""
        # Create first user
        user_data = {
            "username": "testuser",
            "email": "test1@example.com",
            "full_name": "Test User 1",
            "password": "password123"
        }
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        
        # Try to create user with same username
        duplicate_data = {
            "username": "testuser",  # Duplicate username
            "email": "test2@example.com",
            "full_name": "Test User 2",
            "password": "password456"
        }
        response = client.post("/api/v1/users/", json=duplicate_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_user_registration_duplicate_email(self, client, test_db):
        """Test user registration with duplicate email."""
        # Create first user
        user_data = {
            "username": "testuser1",
            "email": "test@example.com",
            "full_name": "Test User 1",
            "password": "password123"
        }
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        
        # Try to create user with same email
        duplicate_data = {
            "username": "testuser2",
            "email": "test@example.com",  # Duplicate email
            "full_name": "Test User 2",
            "password": "password456"
        }
        response = client.post("/api/v1/users/", json=duplicate_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_user_login_valid_credentials(self, client, test_db):
        """Test user login with valid credentials via /api/v1/auth/token."""
        # Create a user first
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("password123")
        )
        test_db.add(user)
        test_db.commit()
        
        # Login using OAuth2 form data
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 200
        
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"
    
    def test_user_login_invalid_username(self, client, test_db):
        """Test user login with invalid username."""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_user_login_invalid_password(self, client, test_db):
        """Test user login with invalid password."""
        # Create a user first
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("correctpassword")
        )
        test_db.add(user)
        test_db.commit()
        
        # Login with wrong password
        login_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_get_current_user_with_valid_token(self, client, authenticated_headers):
        """Test getting current user with valid authentication token."""
        response = client.get("/api/v1/users/me", headers=authenticated_headers)
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["username"] == "testuser"
        assert "password" not in response_data
        assert "hashed_password" not in response_data
    
    def test_get_current_user_without_token(self, client):
        """Test getting current user without authentication token."""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
    
    def test_get_current_user_with_invalid_token(self, client):
        """Test getting current user with invalid authentication token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == 401
    
    def test_protected_endpoint_access(self, client, authenticated_headers, test_db):
        """Test accessing protected endpoints with authentication."""
        response = client.get("/api/v1/users/", headers=authenticated_headers)
        assert response.status_code == 200
    
    def test_login_form_data_oauth2_standard(self, client, test_db):
        """Test that login accepts form data (OAuth2 standard)."""
        # Create a user first
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("password123")
        )
        test_db.add(user)
        test_db.commit()
        
        # Test form data (standard OAuth2)
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 200
        
        # Verify token structure
        response_data = response.json()
        assert "access_token" in response_data
        assert "token_type" in response_data
        assert response_data["token_type"] == "bearer"
    
    def test_token_authentication_flow(self, client, test_db):
        """Test complete authentication flow: register -> login -> access protected."""
        # 1. Register user
        user_data = {
            "username": "flowuser",
            "email": "flow@example.com",
            "full_name": "Flow User",
            "password": "password123"
        }
        register_response = client.post("/api/v1/users/", json=user_data)
        assert register_response.status_code == 201
        
        # 2. Login to get token
        login_data = {
            "username": "flowuser",
            "password": "password123"
        }
        login_response = client.post("/api/v1/auth/token", data=login_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # 3. Use token to access protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        protected_response = client.get("/api/v1/users/me", headers=headers)
        assert protected_response.status_code == 200
        assert protected_response.json()["username"] == "flowuser"
