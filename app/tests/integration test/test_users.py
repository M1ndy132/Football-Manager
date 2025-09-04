"""
Integration tests for user endpoints.
"""

import pytest
from app.database.models import User
from app.core.security import get_password_hash


class TestUserEndpoints:
    """Test user-related endpoints."""
    
    def test_get_all_users(self, client, test_db, authenticated_headers):
        """Test getting all users."""
        # Create some test users
        users_data = [
            {"username": "user1", "email": "user1@test.com", "full_name": "User One"},
            {"username": "user2", "email": "user2@test.com", "full_name": "User Two"},
        ]
        
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash("password123")
            )
            test_db.add(user)
        test_db.commit()
        
        response = client.get("/users/", headers=authenticated_headers)
        assert response.status_code == 200
        
        response_data = response.json()
        assert len(response_data) >= 2  # At least our test users
        
        # Check that passwords are not included
        for user in response_data:
            assert "password" not in user
            assert "hashed_password" not in user
            assert "username" in user
            assert "email" in user
    
    def test_get_user_by_id_existing(self, client, test_db, authenticated_headers):
        """Test getting a user by existing ID."""
        # Create a test user
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("password123")
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        response = client.get(f"/users/{user.id}", headers=authenticated_headers)
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["id"] == user.id
        assert response_data["username"] == "testuser"
        assert response_data["email"] == "test@example.com"
        assert "password" not in response_data
        assert "hashed_password" not in response_data
    
    def test_get_user_by_id_nonexistent(self, client, authenticated_headers):
        """Test getting a user by non-existent ID."""
        response = client.get("/users/999999", headers=authenticated_headers)
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
    
    def test_create_user_valid_data(self, client, test_db):
        """Test creating a user with valid data."""
        user_data = {
            "username": "newuser",
            "email": "new@example.com",
            "full_name": "New User",
            "password": "password123"
        }
        
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        
        response_data = response.json()
        assert response_data["username"] == "newuser"
        assert response_data["email"] == "new@example.com"
        assert response_data["full_name"] == "New User"
        assert "id" in response_data
        assert "password" not in response_data
        
        # Verify user was created in database
        user = test_db.query(User).filter(User.username == "newuser").first()
        assert user is not None
        assert user.email == "new@example.com"
    
    def test_create_user_invalid_email(self, client):
        """Test creating a user with invalid email."""
        user_data = {
            "username": "newuser",
            "email": "invalid-email",
            "full_name": "New User",
            "password": "password123"
        }
        
        response = client.post("/users/", json=user_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_user_missing_required_field(self, client):
        """Test creating a user with missing required field."""
        user_data = {
            "email": "new@example.com",
            "full_name": "New User",
            "password": "password123"
            # Missing username
        }
        
        response = client.post("/users/", json=user_data)
        assert response.status_code == 422  # Validation error
    
    def test_update_user_valid_data(self, client, test_db, authenticated_headers):
        """Test updating a user with valid data."""
        # Create a test user
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("password123")
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        update_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "full_name": "Updated User"
        }
        
        response = client.put(f"/users/{user.id}", json=update_data, headers=authenticated_headers)
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["username"] == "updateduser"
        assert response_data["email"] == "updated@example.com"
        assert response_data["full_name"] == "Updated User"
    
    def test_update_user_nonexistent(self, client, authenticated_headers):
        """Test updating a non-existent user."""
        update_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "full_name": "Updated User"
        }
        
        response = client.put("/users/999999", json=update_data, headers=authenticated_headers)
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
    
    def test_delete_user_existing(self, client, test_db, authenticated_headers):
        """Test deleting an existing user."""
        # Create a test user
        user = User(
            username="deleteuser",
            email="delete@example.com",
            full_name="Delete User",
            hashed_password=get_password_hash("password123")
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        user_id = user.id
        
        response = client.delete(f"/users/{user_id}", headers=authenticated_headers)
        assert response.status_code == 200
        
        # Verify user was deleted from database
        deleted_user = test_db.query(User).filter(User.id == user_id).first()
        assert deleted_user is None
    
    def test_delete_user_nonexistent(self, client, authenticated_headers):
        """Test deleting a non-existent user."""
        response = client.delete("/users/999999", headers=authenticated_headers)
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
    
    def test_get_users_without_authentication(self, client):
        """Test accessing user endpoints without authentication."""
        response = client.get("/users/")
        # This might be allowed or might require authentication
        # Adjust based on your security requirements
        assert response.status_code in [200, 401]
    
    def test_user_pagination(self, client, test_db, authenticated_headers):
        """Test user pagination if implemented."""
        # Create multiple users
        for i in range(15):
            user = User(
                username=f"user{i}",
                email=f"user{i}@test.com",
                full_name=f"User {i}",
                hashed_password=get_password_hash("password123")
            )
            test_db.add(user)
        test_db.commit()
        
        # Test pagination parameters if your API supports them
        response = client.get("/users/?limit=5&offset=0", headers=authenticated_headers)
        if response.status_code == 200:
            response_data = response.json()
            # Check if pagination is working
            if isinstance(response_data, list):
                assert len(response_data) <= 5
    
    def test_user_search_functionality(self, client, test_db, authenticated_headers):
        """Test user search functionality if implemented."""
        # Create test users with searchable data
        users_data = [
            {"username": "alice", "email": "alice@test.com", "full_name": "Alice Johnson"},
            {"username": "bob", "email": "bob@test.com", "full_name": "Bob Smith"},
            {"username": "charlie", "email": "charlie@test.com", "full_name": "Charlie Brown"},
        ]
        
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash("password123")
            )
            test_db.add(user)
        test_db.commit()
        
        # Test search by username if supported
        response = client.get("/users/?search=alice", headers=authenticated_headers)
        if response.status_code == 200:
            response_data = response.json()
            if isinstance(response_data, list):
                # Check if search results contain expected user
                usernames = [user["username"] for user in response_data]
                assert "alice" in usernames
