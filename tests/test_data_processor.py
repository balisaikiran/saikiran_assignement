"""Test cases for DataProcessor."""
import pytest
import pandas as pd
from src.data.processor import DataProcessor

@pytest.fixture
def sample_data():
    """Create sample taxi trip data."""
    return pd.DataFrame({
        'vendor_id': ['A', 'B', 'C', 'D'],
        'pickup_datetime': ['2023-01-01 10:00:00'] * 4,
        'dropoff_datetime': ['2023-01-01 11:00:00'] * 4,
        'passenger_count': [1, 2, None, 2],
        'pickup_longitude': [-73.9876, 0, -73.9876, -73.9876],
        'pickup_latitude': [40.7545, 40.7545, 0, 40.7545],
        'dropoff_longitude': [-74.0065, -74.0065, -74.0065, -74.0065],
        'dropoff_latitude': [40.7406, 40.7406, 40.7406, 40.7406],
        'trip_duration': [3600, 90000, 3600, 3600]
    })

def test_clean_data(sample_data):
    """Test data cleaning functionality."""
    processor = DataProcessor()
    cleaned_data = processor.clean_data(sample_data)
    
    # Should remove rows with missing values
    assert len(cleaned_data) < len(sample_data)
    
    # Should remove rows with invalid coordinates
    assert not any(cleaned_data['pickup_longitude'] == 0)
    assert not any(cleaned_data['pickup_latitude'] == 0)
    
    # Should remove outlier trip durations
    assert all(cleaned_data['trip_duration'] <= 86400)

def test_to_models(sample_data):
    """Test conversion to database models."""
    processor = DataProcessor()
    cleaned_data = processor.clean_data(sample_data)
    models = processor.to_models(cleaned_data)
    
    assert len(models) == len(cleaned_data)
    assert all(hasattr(model, 'vendor_id') for model in models)
    assert all(hasattr(model, 'trip_duration') for model in models)