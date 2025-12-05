from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://codeforces:codeforces_dev@localhost:5432/codeforces_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Auth Service
    AUTH_SERVICE_URL: str = "http://auth-service:8000"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

