"""Database connection management with connection pooling."""

from typing import Generator, AsyncGenerator, Optional
from contextlib import contextmanager, asynccontextmanager
from sqlalchemy import create_engine, event, pool, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
import logging

from .config import db_settings
from .base import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Centralized database connection manager with connection pooling."""
    
    def __init__(self):
        """Initialize database manager."""
        self._engine = None
        self._async_engine = None
        self._session_factory = None
        self._async_session_factory = None
        self._initialized = False
    
    def initialize(self):
        """Initialize database engines and session factories."""
        if self._initialized:
            logger.warning("DatabaseManager already initialized")
            return
        
        try:
            # Log connection info
            conn_info = db_settings.get_connection_info()
            logger.info(f"Initializing database connection to {conn_info.get('location', 'unknown')}")
            
            # Create synchronous engine with connection pooling
            self._engine = create_engine(
                db_settings.get_sync_url(),
                poolclass=QueuePool,
                pool_size=db_settings.pool_size,
                max_overflow=db_settings.max_overflow,
                pool_timeout=db_settings.pool_timeout,
                pool_recycle=db_settings.pool_recycle,
                pool_pre_ping=db_settings.pool_pre_ping,
                echo=db_settings.echo_sql,
            )
            
            # Create async engine with connection pooling
            self._async_engine = create_async_engine(
                db_settings.get_async_url(),
                poolclass=QueuePool,
                pool_size=db_settings.pool_size,
                max_overflow=db_settings.max_overflow,
                pool_timeout=db_settings.pool_timeout,
                pool_recycle=db_settings.pool_recycle,
                pool_pre_ping=db_settings.pool_pre_ping,
                echo=db_settings.echo_sql,
            )
            
            # Create session factories
            self._session_factory = sessionmaker(
                bind=self._engine,
                class_=Session,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
            
            self._async_session_factory = async_sessionmaker(
                bind=self._async_engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
            
            # Set up event listeners
            self._setup_event_listeners()
            
            self._initialized = True
            logger.info(f"DatabaseManager initialized successfully with pool_size={db_settings.pool_size}")
            
        except Exception as e:
            logger.error(f"Failed to initialize DatabaseManager: {e}")
            raise
    
    def _setup_event_listeners(self):
        """Set up SQLAlchemy event listeners for connection management."""
        
        @event.listens_for(self._engine, "connect")
        def receive_connect(dbapi_conn, connection_record):
            """Log when a connection is created."""
            logger.debug("Database connection established")
        
        @event.listens_for(self._engine, "close")
        def receive_close(dbapi_conn, connection_record):
            """Log when a connection is closed."""
            logger.debug("Database connection closed")
        
        @event.listens_for(self._engine, "checkout")
        def receive_checkout(dbapi_conn, connection_record, connection_proxy):
            """Log when a connection is checked out from the pool."""
            logger.debug("Connection checked out from pool")
        
        @event.listens_for(self._engine, "checkin")
        def receive_checkin(dbapi_conn, connection_record):
            """Log when a connection is returned to the pool."""
            logger.debug("Connection returned to pool")
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get a database session (context manager).
        
        Yields:
            Session: SQLAlchemy session
        """
        if not self._initialized:
            self.initialize()
        
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get an async database session (context manager).
        
        Yields:
            AsyncSession: SQLAlchemy async session
        """
        if not self._initialized:
            self.initialize()
        
        session = self._async_session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Async database session error: {e}")
            raise
        finally:
            await session.close()
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            bool: True if connection is successful
        """
        if not self._initialized:
            self.initialize()
        
        try:
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    async def test_connection_async(self) -> bool:
        """
        Test database connection (async).
        
        Returns:
            bool: True if connection is successful
        """
        if not self._initialized:
            self.initialize()
        
        try:
            async with self._async_engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Async database connection test successful")
            return True
        except Exception as e:
            logger.error(f"Async database connection test failed: {e}")
            return False
    
    def get_pool_status(self) -> dict:
        """
        Get connection pool status.
        
        Returns:
            dict: Pool status information
        """
        if not self._initialized or not self._engine:
            return {"error": "Database not initialized"}
        
        try:
            pool = self._engine.pool
            return {
                "pool_size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "total_connections": pool.size() + pool.overflow(),
                "max_overflow": db_settings.max_overflow,
                "pool_timeout": db_settings.pool_timeout,
            }
        except Exception as e:
            logger.error(f"Failed to get pool status: {e}")
            return {"error": str(e)}
    
    def close(self):
        """Close database connections and cleanup."""
        if self._engine:
            self._engine.dispose()
            logger.info("Synchronous engine disposed")
        
        if self._async_engine:
            # Note: async engine disposal should be awaited
            logger.info("Async engine marked for disposal")
        
        self._initialized = False
        logger.info("DatabaseManager closed")
    
    async def close_async(self):
        """Close database connections and cleanup (async)."""
        if self._async_engine:
            await self._async_engine.dispose()
            logger.info("Async engine disposed")
        
        if self._engine:
            self._engine.dispose()
            logger.info("Synchronous engine disposed")
        
        self._initialized = False
        logger.info("DatabaseManager closed (async)")


# Global database manager instance
db_manager = DatabaseManager()


# Dependency injection helpers for FastAPI
def get_db_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database session.
    
    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db_session)):
            return db.query(Item).all()
    """
    with db_manager.get_session() as session:
        yield session


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for async database session.
    
    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_async_db_session)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with db_manager.get_async_session() as session:
        yield session
