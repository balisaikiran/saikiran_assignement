"""Database models for the TaxiTripDataService."""
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TaxiTrip(Base):
    """Model representing a taxi trip."""
    __tablename__ = 'taxi_trips'

    id = Column(Integer, primary_key=True)
    vendor_id = Column(String)
    pickup_datetime = Column(DateTime)
    dropoff_datetime = Column(DateTime)
    passenger_count = Column(Integer)
    pickup_longitude = Column(Float)
    pickup_latitude = Column(Float)
    dropoff_longitude = Column(Float)
    dropoff_latitude = Column(Float)
    trip_duration = Column(Integer)  # in seconds

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'pickup_datetime': self.pickup_datetime.isoformat(),
            'dropoff_datetime': self.dropoff_datetime.isoformat(),
            'passenger_count': self.passenger_count,
            'pickup_longitude': self.pickup_longitude,
            'pickup_latitude': self.pickup_latitude,
            'dropoff_longitude': self.dropoff_longitude,
            'dropoff_latitude': self.dropoff_latitude,
            'trip_duration': self.trip_duration
        }