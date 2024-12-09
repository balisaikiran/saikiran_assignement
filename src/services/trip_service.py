"""Service layer for taxi trip operations."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database.models import TaxiTrip
from fastapi import HTTPException

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
        try:
            query = self.db.query(TaxiTrip)
            
            if start_date:
                query = query.filter(TaxiTrip.pickup_datetime >= start_date)
            if end_date:
                query = query.filter(TaxiTrip.pickup_datetime <= end_date)
                
            # Add debug logging
            print(f"Executing query: {query}")
            
            trips = query.limit(limit).all()
            
            # Add debug logging
            print(f"Found {len(trips)} trips")
            
            return [trip.to_dict() for trip in trips]  # Convert to dictionary
        except Exception as e:
            import traceback
            print(f"Database error details: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Database error occurred: {str(e)}"
            )
        
    def get_trip_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> dict:
        """Get statistical information about trips."""
        try:
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
                "average_duration": float(avg_duration)
            }
        except Exception as e:
            print(f"Database error in get_trip_stats: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Database error occurred"
            )