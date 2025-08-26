from fastapi import FastAPI
from app.routers import (auth_router, user_router, team_router,player_router, match_router, coach_router,venue_router, referee_router)


app = FastAPI(title="Football League Manager API")

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

@app.get("health")
def health_check():
    return {"status": "healthy"}
