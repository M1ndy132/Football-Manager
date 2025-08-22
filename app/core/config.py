from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Football League Manager API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/football_db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-here"  # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]  # React frontend
    
    class Config:
        
        case_sensitive = True
        env_file = ".env"

settings = Settings()