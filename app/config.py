"""Application Configuration."""

import os
from datetime import timedelta
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Database
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', 5432))
    DB_NAME: str = os.getenv('DB_NAME', 'informer')
    DB_USER: str = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'postgres')
    DB_SCHEMA: str = os.getenv('DB_SCHEMA', 'system')
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL."""
        return (
            f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@'
            f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )
    
    # Security
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')
    TOKEN_EXPIRE_HOURS: int = int(os.getenv('TOKEN_EXPIRE_HOURS', 24))
    
    @property
    def TOKEN_EXPIRE_TIMEDELTA(self) -> timedelta:
        """Get token expiration as timedelta."""
        return timedelta(hours=self.TOKEN_EXPIRE_HOURS)
    
    # Admin
    ADMIN_USERNAME: str = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD', 's4nch3s')
    
    # Server
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 8000))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    RELOAD: bool = os.getenv('RELOAD', 'False').lower() == 'true'
    
    # Environment
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    
    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
