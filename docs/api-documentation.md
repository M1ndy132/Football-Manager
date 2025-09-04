# 📚 API Documentation

## 🌐 Football League Manager API

### Base Information
- **Base URL**: `http://localhost:8000`
- **API Version**: `v1`
- **Authentication**: JWT Bearer Token
- **Content Type**: `application/json`

---

## 🔐 Authentication

### Register User
```http
POST /api/v1/users/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "password": "secure123"
}
```

### Login
```http
POST /api/v1/auth/token
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=secure123
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Authentication Header
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

## 👥 User Management

### Get Current User
```http
GET /api/v1/users/me
Authorization: Bearer {token}
```

### Update User Profile
```http
PUT /api/v1/users/{user_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "email": "newemail@example.com",
  "full_name": "John Updated Doe"
}
```

---

## ⚽ Team Management

### Create Team
```http
POST /api/v1/teams/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Manchester United",
  "coach_name": "Erik ten Hag",
  "founded_year": 1878,
  "home_ground": "Old Trafford"
}
```

### List Teams
```http
GET /api/v1/teams/?skip=0&limit=10
Authorization: Bearer {token}
```

### Get Team by ID
```http
GET /api/v1/teams/1
Authorization: Bearer {token}
```

### Update Team
```http
PUT /api/v1/teams/1
Authorization: Bearer {token}
Content-Type: application/json

{
  "coach_name": "New Coach Name",
  "home_ground": "Updated Stadium"
}
```

### Delete Team
```http
DELETE /api/v1/teams/1
Authorization: Bearer {token}
```

---

## 🏃‍♂️ Player Management

### Register Player
```http
POST /api/v1/players/
Authorization: Bearer {token}
Content-Type: application/json

{
  "team_id": 1,
  "name": "Marcus Rashford",
  "position": "Forward",
  "age": 26
}
```

### List Players
```http
GET /api/v1/players/?skip=0&limit=10
Authorization: Bearer {token}
```

### Search Players
```http
GET /api/v1/players/search?team_id=1&position=Forward&min_age=18&max_age=35
Authorization: Bearer {token}
```

### Update Player
```http
PUT /api/v1/players/1
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Marcus Updated Rashford",
  "position": "Winger",
  "age": 27
}
```

---

## 👨‍🏫 Coach Management

### Register Coach
```http
POST /api/v1/coaches/
Authorization: Bearer {token}
Content-Type: application/json

{
  "team_id": 1,
  "name": "Pep Guardiola",
  "experience_years": 15,
  "specialization": "Tactical Development",
  "nationality": "Spanish"
}
```

### List Coaches
```http
GET /api/v1/coaches/?skip=0&limit=10
Authorization: Bearer {token}
```

### Get Team's Coaches
```http
GET /api/v1/coaches/team/1
Authorization: Bearer {token}
```

---

## 👨‍⚖️ Referee Management

### Register Referee
```http
POST /api/v1/referees/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Howard Webb",
  "experience_years": 20,
  "nationality": "English",
  "qualification_level": "FIFA International"
}
```

### List Referees
```http
GET /api/v1/referees/?skip=0&limit=10
Authorization: Bearer {token}
```

---

## 🏟️ Venue Management

### Register Venue
```http
POST /api/v1/venues/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Wembley Stadium",
  "city": "London",
  "country": "England",
  "capacity": 90000,
  "built_year": 2007
}
```

### List Venues
```http
GET /api/v1/venues/?skip=0&limit=10
Authorization: Bearer {token}
```

### Search Venues
```http
GET /api/v1/venues/search?city=London&min_capacity=50000
Authorization: Bearer {token}
```

---

## ⚽ Match Management

### Schedule Match
```http
POST /api/v1/matches/
Authorization: Bearer {token}
Content-Type: application/json

{
  "team_a_id": 1,
  "team_b_id": 2,
  "match_date": "2024-12-25T15:00:00",
  "venue": "Wembley Stadium"
}
```

### List Matches
```http
GET /api/v1/matches/?skip=0&limit=10
Authorization: Bearer {token}
```

### Update Match Score
```http
PUT /api/v1/matches/1/score
Authorization: Bearer {token}
Content-Type: application/json

{
  "score_team_a": 2,
  "score_team_b": 1
}
```

### Filter Matches
```http
GET /api/v1/matches/filter?from_date=2024-01-01&to_date=2024-12-31&team_id=1
Authorization: Bearer {token}
```

---

## 📊 Analytics & Reporting

### League Standings
```http
GET /api/v1/analytics/standings
Authorization: Bearer {token}
```

**Response:**
```json
{
  "standings": [
    {
      "team_id": 1,
      "team_name": "Manchester United",
      "matches_played": 10,
      "wins": 7,
      "draws": 2,
      "losses": 1,
      "goals_for": 21,
      "goals_against": 8,
      "points": 23
    }
  ]
}
```

### Top Scoring Teams
```http
GET /api/v1/analytics/top-scorers?limit=5
Authorization: Bearer {token}
```

### Team Performance
```http
GET /api/v1/analytics/team-performance/1
Authorization: Bearer {token}
```

### Season Summary
```http
GET /api/v1/analytics/season-summary
Authorization: Bearer {token}
```

---

## 🔍 Search & Filter

### Global Search
```http
GET /api/v1/search?q=manchester&entity_type=team
Authorization: Bearer {token}
```

### Advanced Team Search
```http
GET /api/v1/teams/search?name=manchester&coach=guardiola&founded_after=1900
Authorization: Bearer {token}
```

### Player Filtering
```http
GET /api/v1/players/filter?team_id=1&position=Forward&age_range=20-30
Authorization: Bearer {token}
```

---

## 📋 Response Formats

### Success Response
```json
{
  "data": {
    "id": 1,
    "name": "Manchester United",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
}
```

### Error Response
```json
{
  "error": "Validation failed",
  "details": {
    "age": ["Age must be between 16 and 50"],
    "email": ["Email address is already registered"]
  }
}
```

### Pagination Response
```json
{
  "data": [...],
  "pagination": {
    "skip": 0,
    "limit": 10,
    "total": 25
  }
}
```

---

## 🚨 HTTP Status Codes

| Code | Description | Usage |
|------|-------------|-------|
| 200 | OK | Successful GET/PUT requests |
| 201 | Created | Successful POST requests |
| 204 | No Content | Successful DELETE requests |
| 400 | Bad Request | Validation errors, malformed requests |
| 401 | Unauthorized | Authentication required or failed |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource (unique constraint) |
| 422 | Unprocessable Entity | Pydantic validation errors |
| 500 | Internal Server Error | Server-side errors |

---

## 🔒 Role-Based Access Control

### Admin Role
- Full access to all endpoints
- User management
- System configuration

### Coach Role
- Manage their team's players
- View team and match data
- Limited to own team operations

### Referee Role
- Update match scores
- View match assignments
- Read-only access to teams/players

### User Role
- Read-only access to public data
- View teams, players, matches
- No modification permissions

---

## 🛡️ Rate Limiting

### Limits
- **Authenticated users**: 1000 requests/hour
- **Unauthenticated**: 100 requests/hour
- **Admin users**: Unlimited

### Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

---

## 📝 OpenAPI/Swagger Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Sample cURL Commands

#### Get Bearer Token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
```

#### Create Team
```bash
curl -X POST "http://localhost:8000/api/v1/teams/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name":"Arsenal","coach_name":"Mikel Arteta","founded_year":1886}'
```

#### Get Team Standings
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/standings" \
     -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🧪 Testing the API

### Using Python requests
```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/token",
    data={"username": "admin", "password": "admin123"}
)
token = response.json()["access_token"]

# Use the API
headers = {"Authorization": f"Bearer {token}"}
teams = requests.get("http://localhost:8000/api/v1/teams/", headers=headers)
print(teams.json())
```

### Using httpx (async)
```python
import httpx
import asyncio

async def test_api():
    async with httpx.AsyncClient() as client:
        # Login
        login_response = await client.post(
            "http://localhost:8000/api/v1/auth/token",
            data={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        # Get teams
        headers = {"Authorization": f"Bearer {token}"}
        teams_response = await client.get(
            "http://localhost:8000/api/v1/teams/", 
            headers=headers
        )
        return teams_response.json()

asyncio.run(test_api())
```

This API documentation provides comprehensive coverage of all endpoints, authentication, and usage patterns for the Football League Manager system.
