from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://codeforces:codeforces_dev@localhost:5432/codeforces_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Service URLs
    CONTEST_SERVICE_URL: str = "http://contest-service:8000"
    SUBMISSION_SERVICE_URL: str = "http://submission-service:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

