# 🏗️ Football League Manager – Project Architecture

## 1. Project Overview
The Football League Manager is a backend system for managing football leagues.  
It supports different roles (admin, coach, referee, user) and allows management of teams, players, matches, and results.

### Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: SQLite (development), PostgreSQL (production)
- **ORM**: SQLAlchemy + Alembic (migrations)
- **Auth**: JWT-based authentication with role-based access control
- **Tooling**: GitHub (repos, issues, CI/CD), Pytest (testing), Black/Flake8 (linting/formatting)

---

## 2. Project Structure
football_manager/
│── app/
│ ├── main.py # FastAPI entry point
│ ├── core/ # Config, security, error handling
│ ├── database/ # DB setup, models, migrations
│ ├── schemas/ # Pydantic models
│ ├── repositories/ # Data access (CRUD)
│ ├── services/ # Business logic
│ ├── routers/ # API endpoints
│ └── tests/ # Unit & integration tests
│
└── docs/architecture.md # This document


### Layer Responsibilities
- **Routers (API Layer)** → Define endpoints, delegate to services.
- **Services (Business Logic Layer)** → Enforce rules (e.g., match must have 2 teams).
- **Repositories (Data Layer)** → Raw DB queries and CRUD operations.
- **Schemas (Validation Layer)** → Pydantic models for input/output validation.
- **Core** → Config, error handling, and authentication/security logic.
- **Database** → ORM models, migrations, and session management.

---

## 3. Coding Standards
- **Naming**:
  - Classes → `PascalCase` (`Team`, `PlayerService`)
  - Functions & variables → `snake_case` (`get_team`, `player_count`)
  - Files → `lowercase_with_underscores.py`
- **API Design**:
  - Endpoints are **plural nouns** (`/teams`, `/matches`).
  - Use REST verbs (`GET`, `POST`, `PUT`, `DELETE`) correctly.
- **Formatting**:
  - Use `black` for formatting, `flake8` + `isort` for linting.

---

## 4. Error Handling
- Custom exceptions in `core/exceptions.py`:
  - `EntityNotFoundException` → 404
  - `DuplicateEntityException` → 400
  - `UnauthorizedException` → 401
- Global error handler:
  - Standard JSON format:
    ```json
    { "error": "Entity not found" }
    ```
- Logging:
  - Use Python `logging` module.
  - Include timestamps and request IDs in logs.

---

## 5. Authentication & Authorization

### Strategy
- Authentication uses **JWT tokens**.
- Passwords are hashed with `bcrypt`.
- Tokens include `user_id` and `role`.
- Middleware enforces role-based access.

### Roles & Permissions
| Role      | Permissions |
|-----------|-------------|
| **Admin** | Manage users, teams, matches, referees, venues |
| **Coach** | Manage their own team & players |
| **Referee** | View matches, update match results |
| **User** | View teams, players, fixtures |

---

## 6. Database & Migrations
- **ORM**: SQLAlchemy models in `database/models.py`.
- **Migrations**: Alembic for schema versioning.
- **Seeding**: Script (`database/seed.py`) for initial test data.

### Example Schema
- **Users** → `id, name, email, role, hashed_password`
- **Teams** → `id, name, coach_id`
- **Players** → `id, name, age, position, team_id`
- **Matches** → `id, date, venue_id, team1_id, team2_id, referee_id`
- **Results** → `id, match_id, score_team1, score_team2`
- **Venues** → `id, name, location, capacity`

---

## 7. Development Workflow
- **Branches**:
  - `main` → production-ready
  - `dev` → integration branch
  - `feature/*` → feature branches
- **Pull Requests**:
  - Require at least 1 approval before merge
  - All tests must pass
- **CI/CD**:
  - GitHub Actions runs linting and tests on push/PR.

---

## 8. Testing Strategy
- **Unit Tests** → for services and repositories.
- **Integration Tests** → for routers (API endpoints).
- **Test Database** → SQLite in-memory for tests.
- **Framework** → Pytest.

---

## 9. Tech Lead Responsibilities
- Define and enforce architecture.
- Set up database schema and migrations.
- Implement error handling and auth strategy.
- Maintain coding standards and review PRs.
- Manage CI/CD and code quality tools.
- Guide team members and ensure consistency.

---
