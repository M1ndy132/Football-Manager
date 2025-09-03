"""
Test configuration and fixtures for Football Manager application.
"""

import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database.models import Base
from app.database.session import get_db
from app.core.security import get_password_hash

# Create test database
@pytest.fixture(scope="function")  # Changed from "session" to "function"
def test_engine():
    """Create a test database engine using SQLite in-memory database."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create a test database session with transaction rollback."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with test database."""
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }

@pytest.fixture
def sample_team_data():
    """Sample team data for testing."""
    return {
        "name": "Test FC",
        "coach_name": "Test Coach",
        "founded_year": 2000,
        "home_ground": "Test Stadium"
    }

@pytest.fixture
def sample_player_data():
    """Sample player data for testing."""
    return {
        "team_id": 1,
        "name": "Test Player",
        "position": "Forward",
        "age": 25
    }

@pytest.fixture
def sample_venue_data():
    """Sample venue data for testing."""
    return {
        "name": "Test Stadium",
        "city": "Test City",
        "country": "Test Country",
        "capacity": 50000,
        "built_year": 2010
    }

@pytest.fixture
def sample_match_data():
    """Sample match data for testing."""
    from datetime import datetime, timedelta
    return {
        "team_a_id": 1,
        "team_b_id": 2,
        "match_date": datetime.now() + timedelta(days=7),
        "venue": "Test Stadium",
        "score_team_a": 0,
        "score_team_b": 0
    }

@pytest.fixture
def authenticated_headers(client, test_db, sample_user_data):
    """Create authenticated headers for testing protected endpoints."""
    from app.database.models import User
    
    # Create test user
    user = User(
        username=sample_user_data["username"],
        email=sample_user_data["email"],
        full_name=sample_user_data["full_name"],
        hashed_password=get_password_hash(sample_user_data["password"])
    )
    test_db.add(user)
    test_db.commit()
    
    # Login to get token
    login_data = {
        "username": sample_user_data["username"],
        "password": sample_user_data["password"]
    }
    response = client.post("/api/v1/auth/token", data=login_data)
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}

