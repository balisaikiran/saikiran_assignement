"""Application configuration management."""
import os
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/taxi_db"
    )
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://redis:6380/0"
    )
    
    # API Settings
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"
    
    # Authentication
    JWT_SECRET_KEY: str = "your-secret-key"  # Change in production
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Monitoring
    ENABLE_METRICS: bool = True
    PROMETHEUS_PORT: int = 9090
    
    # Cache Settings
    REDIS_URL: Optional[str] = None
    CACHE_TTL: int = 3600  # 1 hour
    
    class Config:
        """Pydantic config class."""
        env_file = ".env"