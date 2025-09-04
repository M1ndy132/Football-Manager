
# 🏗️ Football League Manager – Project Architecture

## 1. Project Overview
The Football League Manager is a backend system for managing football leagues.  
It supports multiple roles (admin, coach, referee, user) and allows management of teams, players, matches, and venues.

### Tech Stack
- **Backend**: FastAPI (Python 3.11+)
- **Database**: SQLite (development), PostgreSQL (production ready)
- **ORM**: SQLAlchemy + Alembic (migrations)
- **Auth**: JWT-based authentication with bcrypt password hashing
- **Code Quality**: Black (formatting), isort (import sorting), flake8 (linting), mypy (type checking)
- **Testing**: pytest with comprehensive unit and integration test suites
- **CI/CD**: GitHub Actions with automated testing, code quality checks, and security scanning

---

## 2. Project Structure
```
football_manager/
│── app/
│   ├── main.py                 # FastAPI entry point
│   │
│   ├── core/                   # Config, security, error handling
│   │   ├── config.py
│   │   ├── security.py
│   │   └── exceptions.py
│   │
│   ├── database/               # Database layer
│   │   ├── session.py          # DB connection
│   │   └── models.py           # All SQLAlchemy models:
│   │         ├── user.py
│   │         ├── team.py
│   │         ├── player.py
│   │         ├── coach.py
│   │         ├── referee.py
│   │         ├── match.py      # Includes score_team1, score_team2, winner_id
│   │         └── venue.py
│   │
│   ├── schemas/                # Pydantic models
│   │   ├── user.py
│   │   ├── team.py
│   │   ├── player.py
│   │   ├── coach.py
│   │   ├── referee.py
│   │   ├── match.py
│   │   └── venue.py
│   │
│   ├── services/               # Business logic + DB operations
│   │   ├── auth_service.py
│   │   ├── team_service.py
│   │   ├── player_service.py
│   │   ├── coach_service.py
│   │   ├── referee_service.py
│   │   ├── match_service.py
│   │   └── venue_service.py
│   │
│   ├── routers/                # API endpoints
│   │   ├── auth_router.py
│   │   ├── user_router.py
│   │   ├── team_router.py
│   │   ├── player_router.py
│   │   ├── coach_router.py
│   │   ├── referee_router.py
│   │   ├── match_router.py
│   │   └── venue_router.py
│   │
│   └── tests/                  # Unit & integration tests
│       ├── test_users.py
│       ├── test_teams.py
│       ├── test_players.py
│       ├── test_coaches.py
│       ├── test_referees.py
│       ├── test_matches.py
│       └── test_venues.py
│
│
└── docs/architecture.md # This document
└── football.db                 # SQLite DB for development
```

---

## 3. Layers & Responsibilities
| Layer       | Responsibility |
|------------|----------------|
| **Routers** | Define endpoints, handle requests, call services |
| **Services** | Business logic + CRUD directly with SQLAlchemy |
| **Schemas** | Pydantic models for request/response validation |
| **Database** | SQLAlchemy models, DB session, migrations |
| **Core** | Config, error handling, security/auth utilities |
| **Tests** | Unit & integration tests for all layers |

---

## 4. Coding Standards & Quality Tools
- **Naming**:
  - Classes → `PascalCase` (`Team`, `PlayerService`)
  - Functions & variables → `snake_case` (`get_team`, `player_count`)
  - Files → `lowercase_with_underscores.py`
- **API Design**:
  - Endpoints are **plural nouns** (`/teams`, `/matches`)
  - Use REST verbs (`GET`, `POST`, `PUT`, `DELETE`) correctly
- **Code Quality**:
  - **Black**: Code formatting with 127-character line length
  - **isort**: Import sorting with Black-compatible profile configuration
  - **flake8**: Linting with custom configuration excluding virtual environments
  - **mypy**: Type checking for better code reliability
- **Configuration Files**:
  - `.flake8`: Excludes `.venv`, `alembic`, and build directories
  - `pyproject.toml`: isort configuration with Black compatibility profile

---

## 5. Error Handling
- **Custom exceptions** in `core/exceptions.py`:
  - `EntityNotFoundException` → 404
  - `DuplicateEntityException` → 400
  - `UnauthorizedException` → 401
- **Global exception handler** returns JSON:
```json
{ "error": "Entity not found" }
```
- **Logging**: timestamps + request IDs using Python `logging` module

---

## 6. Authentication & Authorization
- **JWT tokens** for authentication
- **Password hashing** with `bcrypt`
- **Roles embedded in JWT**: Admin, Coach, Referee, User
- **Middleware** checks token validity and role before allowing access

### Roles & Permissions
| Role      | Permissions |
|-----------|-------------|
| **Admin** | Manage users, teams, matches, referees, venues |
| **Coach** | Manage their own team & players |
| **Referee** | View matches, update match scores |
| **User** | View teams, players, fixtures |

---

## 7. Database Schema Highlights
- **Users** → `id, name, email, role, hashed_password`
- **Teams** → `id, name, coach_id`
- **Players** → `id, name, age, position, team_id`
- **Coaches** → `id, user_id, license_info`
- **Referees** → `id, user_id, certification_level`
- **Matches** → `id, date, venue_id, team1_id, team2_id, referee_id, score_team1, score_team2, winner_id`
- **Venues** → `id, name, location, capacity`

---

## 8. Development Workflow
- **Branches**:
  - `main` → production-ready
  - `dev` → integration branch
  - `feature/*` → feature branches
- **Pull Requests**:
  - Require at least 1 approval before merge
  - All tests must pass
- **CI/CD**:
  - GitHub Actions runs on Python 3.11 and 3.12
  - Automated testing with PYTHONPATH configuration
  - Code quality checks (black, isort, flake8, mypy)
  - Security scanning (safety, bandit)
  - Dependency monitoring and updates

---

## 9. Testing Strategy
- **Unit Tests** → services, database operations, and individual components
- **Integration Tests** → routers, API endpoints, and complete workflows  
- **Test Database** → SQLite in-memory for testing isolation
- **Framework** → pytest with fixtures and async support
- **Coverage** → pytest-cov for test coverage reporting
- **Test Structure**:
  - `app/tests/unit test/` → Component-level tests
  - `app/tests/integration test/` → API endpoint tests
  - `conftest.py` → Shared fixtures and test configuration

---

## 10. Tech Lead Responsibilities
- Define and enforce architecture
- Implement error handling and auth strategy
- Maintain coding standards and review PRs
- Guide team members and ensure consistency
- Set up database and migrations
- Oversee CI/CD and code quality tools

