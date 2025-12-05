"""Database configuration settings."""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    # Database connection
    database_url: str = "postgresql://ai_agents_user:password@localhost:5432/ai_agents"
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
        env_prefix = "DB_"
        case_sensitive = False
    
    def get_sync_url(self) -> str:
        """
        Get synchronous database URL.
        
        Returns:
            str: Synchronous database connection URL
        """
        return self.database_url
    
    def get_async_url(self) -> str:
        """
        Get async database URL.
        
        Returns:
            str: Async database connection URL
        """
        if self.async_database_url:
            return self.async_database_url
        
        # Convert postgresql:// to postgresql+asyncpg://
        if self.database_url.startswith("postgresql://"):
            return self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif self.database_url.startswith("postgres://"):
            return self.database_url.replace("postgres://", "postgresql+asyncpg://", 1)
        
        return self.database_url
    
    def get_connection_info(self) -> dict:
        """
        Get database connection information (for logging/debugging).
        
        Returns:
            dict: Connection information without sensitive data
        """
        url = self.database_url
        # Parse URL to extract components (hide password)
        if "://" in url:
            protocol, rest = url.split("://", 1)
            if "@" in rest:
                credentials, location = rest.split("@", 1)
                user = credentials.split(":")[0] if ":" in credentials else credentials
                host_port_db = location
            else:
                user = "unknown"
                host_port_db = rest
            
            return {
                "protocol": protocol,
                "user": user,
                "location": host_port_db,
                "pool_size": self.pool_size,
                "max_overflow": self.max_overflow,
            }
        
        return {
            "url": "invalid",
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
        }


# Global settings instance
db_settings = DatabaseSettings()
