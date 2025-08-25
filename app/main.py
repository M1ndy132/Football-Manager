from fastapi import FastAPI
from app.routers import team_router, player_router

 


app = FastAPI(title="Football League Manager API")

app.include_router(team_router.router)
app.include_router(player_router.router)

@app.get("/")
def root():
    return {"message": "API is working! Welcome to Football League Manager"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
