# 🧪 Test Documentation & Instructions

## 📋 Test Overview

The Football League Manager project implements comprehensive testing with **38 unit tests** covering models and schemas, plus integration test capabilities.

### Test Framework Stack
- **pytest**: Primary testing framework
- **pytest-asyncio**: Async testing support
- **pytest-cov**: Code coverage reporting
- **pytest-mock**: Mocking utilities
- **httpx**: HTTP client for API testing
- **SQLAlchemy**: In-memory database for testing

---

## 🏗️ Test Structure

```
app/tests/
├── unit test/
│   ├── conftest.py          # Test configuration & fixtures
│   ├── test_model.py        # Database model tests (17 tests)
│   └── test_schemas.py      # Pydantic schema tests (21 tests)
├── test_auth.py            # Authentication tests
├── test_coaches.py         # Coach service tests
├── test_matches.py         # Match service tests
├── test_players.py         # Player service tests  
├── test_referees.py        # Referee service tests
├── test_users.py           # User service tests
└── test_venue.py           # Venue service tests
```

---

## 🚀 Running Tests

### Run All Tests
```bash
# Basic test run
pytest

# Verbose output with short traceback
pytest -v --tb=short

# Run specific test directory
pytest "app/tests/unit test/" -v
```

### Run Specific Test Categories
```bash
# Run only model tests
pytest app/tests/unit\ test/test_model.py -v

# Run only schema tests
pytest app/tests/unit\ test/test_schemas.py -v

# Run specific test class
pytest app/tests/unit\ test/test_model.py::TestTeamModel -v

# Run specific test method
pytest app/tests/unit\ test/test_model.py::TestTeamModel::test_create_team_valid_data -v
```

### Coverage Reporting
```bash
# Generate coverage report
pytest --cov=app --cov-report=html --cov-report=term

# Coverage with specific directory
pytest "app/tests/unit test/" --cov=app --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

### CI/CD Testing
```bash
# Run tests as in CI pipeline
pytest "app/tests/unit test/" -v --tb=short
```

---

## 🧪 Test Categories

### 1. **Model Tests** (`test_model.py`)

**Purpose**: Test SQLAlchemy database models  
**Coverage**: 17 tests across 7 model classes

#### Team Model Tests
```python
def test_create_team_valid_data(db):
    """Test creating team with valid data"""
    
def test_team_name_unique_constraint(db):
    """Test team name uniqueness constraint"""
    
def test_team_founded_year_constraint(db):
    """Test founded year validation (> 1800)"""
```

#### User Model Tests
```python
def test_create_user_valid_data(db):
    """Test user creation with valid data"""
    
def test_user_username_unique_constraint(db):
    """Test username uniqueness"""
    
def test_user_email_unique_constraint(db):
    """Test email uniqueness"""
```

#### Player Model Tests
```python
def test_create_player_valid_data(db):
    """Test player creation with team assignment"""
    
def test_player_age_constraint(db):
    """Test age constraint (16-50 years)"""
```

### 2. **Schema Tests** (`test_schemas.py`)

**Purpose**: Test Pydantic validation schemas  
**Coverage**: 21 tests across schema validation

#### Validation Tests
```python
def test_user_create_invalid_email():
    """Test email validation handling"""
    
def test_player_create_invalid_age():
    """Test age range validation"""
    
def test_venue_create_negative_capacity():
    """Test capacity validation (must be positive)"""
```

#### Serialization Tests
```python
def test_team_response_serialization():
    """Test team data serialization"""
    
def test_user_response_excludes_password():
    """Test password exclusion in responses"""
```

---

## 🔧 Test Configuration

### `conftest.py` Setup
```python
@pytest.fixture(scope="function")
def db():
    """Create in-memory SQLite database for each test"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

@pytest.fixture
def sample_team_data():
    """Sample team data for testing"""
    return {
        "name": "Test Team",
        "coach_name": "Test Coach",
        "founded_year": 2000,
        "home_ground": "Test Stadium"
    }
```

### pytest Configuration (`pyproject.toml`)
```toml
[tool.pytest.ini_options]
testpaths = ["app/tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--strict-config",
    "--disable-warnings"
]
asyncio_mode = "auto"
```

---

## 📊 Current Test Results

### Test Summary
```
================================ test session starts ================================
collected 38 items

app/tests/unit test/test_model.py::TestTeamModel::test_create_team_valid_data PASSED
app/tests/unit test/test_model.py::TestTeamModel::test_team_name_unique_constraint PASSED
app/tests/unit test/test_model.py::TestTeamModel::test_team_founded_year_constraint PASSED
app/tests/unit test/test_model.py::TestUserModel::test_create_user_valid_data PASSED
...
============================== 38 passed, 18 warnings in 1.29s ==============================
```

### Coverage Report
- **Lines Covered**: 85%+ across core modules
- **Models**: 100% coverage on critical paths
- **Schemas**: 95%+ validation coverage
- **Services**: 80%+ business logic coverage

---

## 🌐 Integration Testing

### API Testing Framework
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_team_endpoint():
    response = client.post(
        "/api/v1/teams/",
        json={"name": "Test Team", "founded_year": 2000},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Team"
```

### Database Integration Tests
```python
def test_team_player_relationship(db):
    """Test one-to-many relationship between teams and players"""
    # Create team
    team = Team(name="Arsenal", founded_year=1886)
    db.add(team)
    db.commit()
    
    # Create players for team
    player1 = Player(team_id=team.id, name="Player 1", position="Forward", age=25)
    player2 = Player(team_id=team.id, name="Player 2", position="Defender", age=28)
    
    db.add_all([player1, player2])
    db.commit()
    
    # Verify relationship
    team_players = db.query(Player).filter(Player.team_id == team.id).all()
    assert len(team_players) == 2
```

---

## 🚨 Error Testing

### Constraint Validation Tests
```python
def test_negative_age_raises_error(db):
    """Test that negative age raises validation error"""
    with pytest.raises(IntegrityError):
        player = Player(name="Test", position="Forward", age=-5, team_id=1)
        db.add(player)
        db.commit()

def test_duplicate_team_name_error(db):
    """Test unique constraint on team names"""
    team1 = Team(name="Duplicate Team", founded_year=2000)
    team2 = Team(name="Duplicate Team", founded_year=2001)
    
    db.add(team1)
    db.commit()
    
    with pytest.raises(IntegrityError):
        db.add(team2)
        db.commit()
```

### Schema Validation Tests
```python
def test_invalid_email_format():
    """Test email validation"""
    with pytest.raises(ValidationError):
        UserCreate(
            username="test",
            email="invalid-email",
            password="password123"
        )

def test_age_out_of_range():
    """Test player age validation"""
    with pytest.raises(ValidationError):
        PlayerCreate(
            team_id=1,
            name="Test Player",
            position="Forward",
            age=15  # Below minimum age
        )
```

---

## 🔍 Test Data Management

### Test Database
- **Engine**: In-memory SQLite for speed
- **Isolation**: Each test gets fresh database
- **Cleanup**: Automatic cleanup after each test
- **Seeding**: Controlled test data injection

### Sample Data Fixtures
```python
@pytest.fixture
def sample_teams(db):
    """Create sample teams for testing"""
    teams = [
        Team(name="Arsenal", founded_year=1886),
        Team(name="Chelsea", founded_year=1905),
        Team(name="Liverpool", founded_year=1892)
    ]
    db.add_all(teams)
    db.commit()
    return teams

@pytest.fixture
def authenticated_user():
    """Create authenticated user for API tests"""
    return {
        "username": "testuser",
        "token": "mock-jwt-token"
    }
```

---

## 🚀 Performance Testing

### Load Testing
```python
import asyncio
import httpx

async def load_test_teams_endpoint():
    """Load test the teams endpoint"""
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(100):
            task = client.get("http://localhost:8000/api/v1/teams/")
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        success_count = sum(1 for r in responses if r.status_code == 200)
        print(f"Successful requests: {success_count}/100")
```

### Database Performance Tests
```python
def test_bulk_insert_performance(db):
    """Test bulk insertion performance"""
    import time
    
    start_time = time.time()
    
    # Insert 1000 players
    players = [
        Player(name=f"Player {i}", position="Forward", age=20+i%15, team_id=1)
        for i in range(1000)
    ]
    
    db.add_all(players)
    db.commit()
    
    end_time = time.time()
    duration = end_time - start_time
    
    assert duration < 5.0  # Should complete within 5 seconds
    assert db.query(Player).count() == 1000
```

---

## 📈 Test Maintenance

### Adding New Tests
1. **Model Tests**: Add to `test_model.py` with appropriate test class
2. **Schema Tests**: Add to `test_schemas.py` with validation scenarios
3. **Service Tests**: Create new test file following naming convention
4. **Integration Tests**: Add to appropriate service test file

### Test Naming Convention
```python
# Pattern: test_[action]_[scenario]_[expected_result]
def test_create_team_valid_data_success():
    """Clear description of what this test validates"""
    pass

def test_create_team_duplicate_name_raises_error():
    """Test duplicate team name constraint"""
    pass

def test_update_player_nonexistent_id_returns_404():
    """Test updating non-existent player"""
    pass
```

### Best Practices
- ✅ **One assertion per test** (when possible)
- ✅ **Descriptive test names** explaining the scenario
- ✅ **Clear test documentation** with docstrings
- ✅ **Independent tests** that don't depend on each other
- ✅ **Clean test data** using fixtures and teardown
- ✅ **Edge case testing** for boundary conditions
- ✅ **Error condition testing** for failure scenarios

---

## 🔄 Continuous Integration

### GitHub Actions Test Pipeline
```yaml
- name: Run Tests
  run: |
    pytest "app/tests/unit test/" -v --tb=short
    
- name: Generate Coverage Report
  run: |
    pytest "app/tests/unit test/" --cov=app --cov-report=xml
    
- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

### Test Requirements
- ✅ All tests must pass before merge
- ✅ Coverage threshold: >80%
- ✅ No failing tests in main branch
- ✅ New features require corresponding tests

This comprehensive test documentation ensures reliable, maintainable code with high confidence in system functionality.
