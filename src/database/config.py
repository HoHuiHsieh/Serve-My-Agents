"""Database configuration settings."""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    # Individual database connection components
    postgres_user: str = "ai_agents_user"
    postgres_password: str = "password"
    postgres_db: str = "ai_agents"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    
    # Full database URL (optional - constructed from components if not provided)
    database_url: Optional[str] = None
    async_database_url: Optional[str] = None
    
    # Connection pool settings
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600
    pool_pre_ping: bool = True
    
    # Echo SQL queries (for debugging)
    echo_sql: bool = False
    
    class Config:
        env_file = ".env"
        env_prefix = ""  # No prefix - read POSTGRES_* directly
        case_sensitive = False
        extra = "ignore"  # Allow extra env vars without validation errors
    
    def get_sync_url(self) -> str:
        """
        Get synchronous database URL.
        
        Returns:
            str: Synchronous database connection URL
        """
        if self.database_url:
            return self.database_url
        
        # Construct from components
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    def get_async_url(self) -> str:
        """
        Get async database URL.
        
        Returns:
            str: Async database connection URL
        """
        if self.async_database_url:
            return self.async_database_url
        
        sync_url = self.get_sync_url()
        
        # Convert postgresql:// to postgresql+asyncpg://
        if sync_url.startswith("postgresql://"):
            return sync_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif sync_url.startswith("postgres://"):
            return sync_url.replace("postgres://", "postgresql+asyncpg://", 1)
        
        return sync_url
    
    def get_connection_info(self) -> dict:
        """
        Get database connection information (for logging/debugging).
        
        Returns:
            dict: Connection information without sensitive data
        """
        return {
            "protocol": "postgresql",
            "user": self.postgres_user,
            "host": self.postgres_host,
            "port": self.postgres_port,
            "database": self.postgres_db,
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
        }


# Global settings instance
db_settings = DatabaseSettings()
