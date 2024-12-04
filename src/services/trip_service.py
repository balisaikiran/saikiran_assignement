"""Service layer for taxi trip operations."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database.models import TaxiTrip

class TripService:
    """Service for handling taxi trip operations."""
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_trips(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[TaxiTrip]:
        """Get trips within a date range."""
        query = self.db.query(TaxiTrip)
        
        if start_date:
            query = query.filter(TaxiTrip.pickup_datetime >= start_date)
        if end_date:
            query = query.filter(TaxiTrip.pickup_datetime <= end_date)
            
        return query.limit(limit).all()
        
    def get_trip_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> dict:
        """Get statistical information about trips."""
        query = self.db.query(TaxiTrip)
        
        if start_date:
            query = query.filter(TaxiTrip.pickup_datetime >= start_date)
        if end_date:
            query = query.filter(TaxiTrip.pickup_datetime <= end_date)
            
        # Basic statistics calculation
        total_trips = query.count()
        avg_duration = query.with_entities(
            func.avg(TaxiTrip.trip_duration)
        ).scalar() or 0
        
        return {
            "total_trips": total_trips,
            "average_duration": avg_duration
        }