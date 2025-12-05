"""Health check utilities for database."""

import logging
from typing import Dict, Any

from .connection import db_manager

logger = logging.getLogger(__name__)


async def check_database_health() -> Dict[str, Any]:
    """
    Check database health status.
    
    Returns:
        dict: Health check results including connection status and pool info
    """
    try:
        # Test connection
        is_connected = await db_manager.test_connection_async()
        
        # Get pool status
        pool_status = db_manager.get_pool_status()
        
        return {
            "status": "healthy" if is_connected else "unhealthy",
            "connected": is_connected,
            "pool": pool_status,
            "details": {
                "initialized": db_manager._initialized,
                "pool_available": pool_status.get("checked_in", 0),
                "pool_in_use": pool_status.get("checked_out", 0),
            }
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "connected": False,
            "error": str(e)
        }


def check_database_health_sync() -> Dict[str, Any]:
    """
    Check database health status (synchronous).
    
    Returns:
        dict: Health check results including connection status and pool info
    """
    try:
        # Test connection
        is_connected = db_manager.test_connection()
        
        # Get pool status
        pool_status = db_manager.get_pool_status()
        
        return {
            "status": "healthy" if is_connected else "unhealthy",
            "connected": is_connected,
            "pool": pool_status,
            "details": {
                "initialized": db_manager._initialized,
                "pool_available": pool_status.get("checked_in", 0),
                "pool_in_use": pool_status.get("checked_out", 0),
            }
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "connected": False,
            "error": str(e)
        }
