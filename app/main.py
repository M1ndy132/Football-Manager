from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers import (
    auth_router,
    coach_router,
    match_router,
    player_router,
    referee_router,
    team_router,
    user_router,
    venue_router,
)

app = FastAPI(
    title="Football League Manager API",
    description="""
    🏈 **Community Football League Manager**
    
    A comprehensive API for managing football leagues, teams, players, and matches.
    
    ## Features
    * **Teams**: Manage football teams and their information
    * **Players**: Track player details and team assignments  
    * **Matches**: Schedule fixtures and record results
    * **Standings**: Calculate league tables and statistics
    * **Authentication**: Secure user management
    
    ## Quick Start
    1. Register a new user at `/api/v1/users/`
    2. Login to get your token at `/api/v1/auth/token`
    3. Use the token to access protected endpoints
    
    **Demo Interface**: Visit `/demo` for a simple web interface
    """,
    version="1.0.0",
    contact={
        "name": "Football League Manager Team",
        "email": "team@footballmanager.com",
    },
)

# Include routers
app.include_router(auth_router.router, prefix="/api/v1", tags=["auth"])
app.include_router(user_router.router, prefix="/api/v1", tags=["users"])
app.include_router(team_router.router, prefix="/api/v1", tags=["teams"])
app.include_router(player_router.router, prefix="/api/v1", tags=["players"])
app.include_router(match_router.router, prefix="/api/v1", tags=["matches"])
app.include_router(coach_router.router, prefix="/api/v1", tags=["coaches"])
app.include_router(venue_router.router, prefix="/api/v1", tags=["venues"])
app.include_router(referee_router.router, prefix="/api/v1", tags=["referees"])


@app.get("/")
def root():
    return {"message": "API is working! Welcome to Football League Manager"}


@app.get("/demo", response_class=HTMLResponse)
def demo_interface():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Football League Manager - Demo</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { background: #1f4e79; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .section { background: #f8f9fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #28a745; }
            .api-link { color: #007bff; text-decoration: none; font-weight: bold; }
            .api-link:hover { text-decoration: underline; }
            .highlight { background: #fff3cd; padding: 10px; border-radius: 4px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏈 Football League Manager</h1>
            <p>Community Football League Management System - Live Demo</p>
        </div>
        
        <div class="section">
            <h2>🚀 Quick Start Guide</h2>
            <div class="highlight">
                <strong>API Documentation:</strong> <a href="/docs" class="api-link">Interactive API Docs</a> | 
                <a href="/redoc" class="api-link">ReDoc Documentation</a>
            </div>
            <ol>
                <li><strong>Explore the API:</strong> Visit <a href="/docs" class="api-link">/docs</a> for interactive testing</li>
                <li><strong>Authentication:</strong> Create a user and get your access token</li>
                <li><strong>Manage Teams:</strong> Add teams, players, and schedule matches</li>
                <li><strong>View Results:</strong> Check league standings and match results</li>
            </ol>
        </div>
        
        <div class="section">
            <h2>📊 Key Features Demo</h2>
            <ul>
                <li><strong>User Management:</strong> <a href="/docs#/users" class="api-link">User CRUD Operations</a></li>
                <li><strong>Team Management:</strong> <a href="/docs#/teams" class="api-link">Team Operations</a></li>
                <li><strong>Player Management:</strong> <a href="/docs#/players" class="api-link">Player Operations</a></li>
                <li><strong>Match Scheduling:</strong> <a href="/docs#/matches" class="api-link">Match Operations</a></li>
                <li><strong>League Standings:</strong> Real-time calculations</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🔧 Technical Stack</h2>
            <ul>
                <li><strong>Backend:</strong> FastAPI + Python 3.12</li>
                <li><strong>Database:</strong> SQLAlchemy + Alembic migrations</li>
                <li><strong>Authentication:</strong> JWT tokens with secure password hashing</li>
                <li><strong>Testing:</strong> Pytest with automated CI/CD</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🎯 API Endpoints</h2>
            <p><strong>Base URL:</strong> <code>http://127.0.0.1:8000</code></p>
            <ul>
                <li><code>POST /api/v1/auth/token</code> - Login and get access token</li>
                <li><code>GET /api/v1/teams/</code> - List all teams</li>
                <li><code>GET /api/v1/players/</code> - List all players</li>
                <li><code>GET /api/v1/matches/</code> - List all matches</li>
                <li><code>GET /api/v1/standings/</code> - League table (if implemented)</li>
            </ul>
        </div>
        
        <script>
            console.log("Football League Manager Demo Loaded");
        </script>
    </body>
    </html>
    """


@app.get("/health")
def health_check():
    return {"status": "healthy"}
