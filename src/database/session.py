"""Database session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..database.models import Base
import os

class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/taxi_db")
db_manager = DatabaseManager(DATABASE_URL)

# Create tables
Base.metadata.create_all(bind=db_manager.engine)

def get_db() -> Session:
    """Get database session."""
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close() 