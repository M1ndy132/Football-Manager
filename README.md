# Football League Manager API

A comprehensive REST API for managing football leagues, teams, players, and matches built with FastAPI and SQLAlchemy.

## 🏆 Project Overview

This Football League Manager API provides a complete backend system for managing football league operations including team management, player registration, match scheduling, and statistical tracking.

## ✨ Features

- **Team Management**: Create and manage football teams with detailed information
- **Player Registry**: Track players with positions, ages, and team assignments
- **Match Scheduling**: Schedule fixtures and record match results
- **Venue Management**: Manage stadiums and their information
- **Coach Profiles**: Track coaching staff and their experience
- **Referee System**: Manage match officials and qualifications
- **User Authentication**: Secure JWT-based authentication system
- **Interactive Documentation**: Auto-generated API documentation with Swagger UI

## 🛠️ Technology Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Documentation**: Auto-generated with Swagger UI
- **Testing**: pytest with comprehensive test suite
- **Validation**: Pydantic schemas

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/M1ndy132/Football-Manager.git
   cd Football-Manager
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows
   # or
   source .venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Initialize database with demo data**
   ```bash
   python seed_data.py
   ```

5. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the application**
   - Demo Interface: http://127.0.0.1:8000/demo
   - API Documentation: http://127.0.0.1:8000/docs
   - API Root: http://127.0.0.1:8000/api/v1

## 📊 Database Schema

The system includes 9 interconnected entities:

- **Teams**: Football team information and home grounds
- **Users**: Authentication and user management
- **Players**: Player profiles with team assignments
- **Coaches**: Coaching staff with experience data
- **Matches**: Match fixtures with scores and venues
- **Venues**: Stadium information and capacity details
- **Referees**: Match officials with qualifications
- **Sponsors**: Sponsorship deals and financial data
- **Managers**: Team management structure

## 🔐 API Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register a user**: `POST /api/v1/users/`
2. **Login**: `POST /api/v1/auth/token`
3. **Use token**: Include `Authorization: Bearer <token>` in headers

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/token` - User login
- `GET /api/v1/users/me` - Get current user

### Teams
- `GET /api/v1/teams/` - List all teams
- `POST /api/v1/teams/` - Create new team
- `GET /api/v1/teams/{id}` - Get team details
- `PUT /api/v1/teams/{id}` - Update team
- `DELETE /api/v1/teams/{id}` - Delete team

### Players
- `GET /api/v1/players/` - List all players
- `POST /api/v1/players/` - Add new player
- `GET /api/v1/players/{id}` - Get player details

### Matches
- `GET /api/v1/matches/` - List all matches
- `POST /api/v1/matches/` - Schedule new match
- `PUT /api/v1/matches/{id}` - Update match results

*[Additional endpoints for venues, coaches, referees]*

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python run_tests.py

# Run specific test file
python -m pytest "app/tests/unit test/schemas.py" -v

# Run with coverage
python -m pytest --cov=app --cov-report=html
```

## 📱 Demo Data

The project includes realistic demo data:
- 8 Premier League teams
- 20+ professional players
- 5 experienced coaches
- 10 matches (completed and upcoming)
- Professional venues and referees

Initialize with: `python seed_data.py`

## 🏗️ Project Structure

```
app/
├── core/           # Core functionality (config, security)
├── database/       # Database models and session management
├── routers/        # API route handlers
├── schemas/        # Pydantic schemas for data validation
├── services/       # Business logic services
└── tests/          # Unit and integration tests
```

## 🔧 Development

### Running in Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Operations
- Models are defined in `app/database/models.py`
- Database session in `app/database/session.py`
- Seed data script: `seed_data.py`

## 📖 Documentation

- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Demo Interface**: http://127.0.0.1:8000/demo
- **Alternative Docs**: http://127.0.0.1:8000/redoc

## 🤝 Contributing

This is an academic project for demonstration purposes.

## 📄 License

Educational project - created for academic demonstration.

## 👨‍💻 Author

**Team Football Manager**
- Academic Project
- Football League Management System

---

**🎯 Ready for Demo**: This project demonstrates comprehensive backend development skills including API design, database modeling, authentication, and professional documentation.