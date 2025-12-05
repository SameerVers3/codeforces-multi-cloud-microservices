from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://codeforces:codeforces_dev@localhost:5432/codeforces_db"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://codeforces:codeforces_dev@localhost:5672/"
    SUBMISSION_QUEUE: str = "submissions"
    
    # Service URLs
    AUTH_SERVICE_URL: str = "http://auth-service:8000"
    CONTEST_SERVICE_URL: str = "http://contest-service:8000"
    EXECUTION_SERVICE_URL: str = "http://execution-service:8000"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

