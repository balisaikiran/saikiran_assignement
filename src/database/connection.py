"""Database connection management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self, connection_url):
        self.engine = create_engine(connection_url)
        self.Session = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        """Create all defined tables."""
        Base.metadata.create_all(self.engine)
        
    def get_session(self):
        """Get a new database session."""
        return self.Session()