"""Test cases for TripService."""
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.services.trip_service import TripService
from src.database.models import Base, TaxiTrip

@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Add test data
    test_trips = [
        TaxiTrip(
            vendor_id='test1',
            pickup_datetime=datetime.now() - timedelta(hours=2),
            dropoff_datetime=datetime.now() - timedelta(hours=1),
            passenger_count=2,
            pickup_longitude=-73.9876,
            pickup_latitude=40.7545,
            dropoff_longitude=-74.0065,
            dropoff_latitude=40.7406,
            trip_duration=3600
        ),
        TaxiTrip(
            vendor_id='test2',
            pickup_datetime=datetime.now() - timedelta(days=1),
            dropoff_datetime=datetime.now() - timedelta(days=1, hours=-1),
            passenger_count=1,
            pickup_longitude=-73.9876,
            pickup_latitude=40.7545,
            dropoff_longitude=-74.0065,
            dropoff_latitude=40.7406,
            trip_duration=7200
        )
    ]
    
    session.bulk_save_objects(test_trips)
    session.commit()
    
    yield session
    
    Base.metadata.drop_all(engine)

def test_get_trips(db_session):
    """Test retrieving trips within a date range."""
    service = TripService(db_session)
    
    # Test without date filters
    trips = service.get_trips()
    assert len(trips) == 2
    
    # Test with date filter
    start_date = datetime.now() - timedelta(hours=3)
    trips = service.get_trips(start_date=start_date)
    assert len(trips) == 1
    assert trips[0].vendor_id == 'test1'

def test_get_trip_stats(db_session):
    """Test calculating trip statistics."""
    service = TripService(db_session)
    
    stats = service.get_trip_stats()
    assert stats['total_trips'] == 2
    assert stats['average_duration'] == 5400  # (3600 + 7200) / 2