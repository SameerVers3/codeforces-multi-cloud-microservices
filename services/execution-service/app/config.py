from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://codeforces:codeforces_dev@localhost:5672/"
    SUBMISSION_QUEUE: str = "submissions"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Docker
    DOCKER_SOCKET: str = "/var/run/docker.sock"
    
    # Execution limits
    MAX_EXECUTION_TIME_SECONDS: int = 10
    MAX_MEMORY_MB: int = 512
    MAX_OUTPUT_SIZE_BYTES: int = 1024 * 1024  # 1MB
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

