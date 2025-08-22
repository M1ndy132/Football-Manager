from fastapi import FastAPI

app = FastAPI(title="Football League Manager API")

@app.get("/")
def root():
    return {"message": "API is working! Welcome to Football League Manager"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
