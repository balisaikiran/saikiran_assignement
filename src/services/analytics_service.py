"""Advanced analytics service for taxi trip data."""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy import func, and_, extract
from sqlalchemy.orm import Session
from ..database.models import TaxiTrip
from ..utils.logging import get_logger
from ..cache.redis_manager import RedisManager

logger = get_logger(__name__)

class AnalyticsService:
    """Service for advanced analytics operations."""
    
    def __init__(self, db: Session, redis_manager: RedisManager):
        self.db = db
        self.redis = redis_manager
    
    async def get_hourly_distribution(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[int, int]:
        """Get hourly distribution of trips."""
        logger.info("Calculating hourly trip distribution")
        
        query = self.db.query(
            func.extract('hour', TaxiTrip.pickup_datetime).label('hour'),
            func.count().label('count')
        )
        
        if start_date:
            query = query.filter(TaxiTrip.pickup_datetime >= start_date)
        if end_date:
            query = query.filter(TaxiTrip.pickup_datetime <= end_date)
            
        result = query.group_by('hour').all()
        return {int(hour): count for hour, count in result}
    
    async def get_popular_routes(
        self,
        limit: int = 10,
        min_trips: int = 5
    ) -> List[Dict]:
        """Get most popular routes."""
        logger.info(f"Finding top {limit} popular routes")
        
        query = self.db.query(
            TaxiTrip.pickup_latitude,
            TaxiTrip.pickup_longitude,
            TaxiTrip.dropoff_latitude,
            TaxiTrip.dropoff_longitude,
            func.count().label('trip_count'),
            func.avg(TaxiTrip.trip_duration).label('avg_duration')
        ).group_by(
            TaxiTrip.pickup_latitude,
            TaxiTrip.pickup_longitude,
            TaxiTrip.dropoff_latitude,
            TaxiTrip.dropoff_longitude
        ).having(
            func.count() >= min_trips
        ).order_by(
            func.count().desc()
        ).limit(limit)
        
        return [
            {
                'pickup': {'lat': r.pickup_latitude, 'lng': r.pickup_longitude},
                'dropoff': {'lat': r.dropoff_latitude, 'lng': r.dropoff_longitude},
                'trip_count': r.trip_count,
                'avg_duration': r.avg_duration
            }
            for r in query.all()
        ]
    
    async def get_peak_hours(
        self,
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """Get peak hours analysis for the last N days."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        query = self.db.query(
            extract('dow', TaxiTrip.pickup_datetime).label('day_of_week'),
            extract('hour', TaxiTrip.pickup_datetime).label('hour'),
            func.count().label('trip_count')
        ).filter(
            and_(
                TaxiTrip.pickup_datetime >= start_date,
                TaxiTrip.pickup_datetime <= end_date
            )
        ).group_by(
            'day_of_week',
            'hour'
        ).order_by(
            'day_of_week',
            'hour'
        )
        
        results = query.all()
        return [
            {
                'day_of_week': int(r.day_of_week),
                'hour': int(r.hour),
                'trip_count': int(r.trip_count)
            }
            for r in results
        ]
    
    async def get_distance_distribution(self) -> List[Tuple[float, int]]:
        """Get distribution of trip distances."""
        query = self.db.query(
            func.round(
                func.sqrt(
                    func.power(TaxiTrip.dropoff_longitude - TaxiTrip.pickup_longitude, 2) +
                    func.power(TaxiTrip.dropoff_latitude - TaxiTrip.pickup_latitude, 2)
                ) * 111.32,  # Convert to kilometers (approximate)
                1
            ).label('distance'),
            func.count().label('count')
        ).group_by(
            'distance'
        ).order_by(
            'distance'
        )
        
        results = query.all()
        return [(float(r.distance), int(r.count)) for r in results]