"""Data processing and ingestion utilities."""
import pandas as pd
from typing import List
from ..database.models import TaxiTrip

class DataProcessor:
    """Handles data processing and cleaning operations."""
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the taxi trip data."""
        # Remove rows with missing values
        df = df.dropna()
        
        # Remove outliers (example: trips longer than 24 hours)
        df = df[df['trip_duration'] <= 86400]
        
        # Remove trips with invalid coordinates
        df = df[
            (df['pickup_longitude'] != 0) &
            (df['pickup_latitude'] != 0) &
            (df['dropoff_longitude'] != 0) &
            (df['dropoff_latitude'] != 0)
        ]
        
        return df
    
    @staticmethod
    def to_models(df: pd.DataFrame) -> List[TaxiTrip]:
        """Convert DataFrame rows to TaxiTrip models."""
        models = []
        for _, row in df.iterrows():
            trip = TaxiTrip(
                vendor_id=row['vendor_id'],
                pickup_datetime=row['pickup_datetime'],
                dropoff_datetime=row['dropoff_datetime'],
                passenger_count=row['passenger_count'],
                pickup_longitude=row['pickup_longitude'],
                pickup_latitude=row['pickup_latitude'],
                dropoff_longitude=row['dropoff_longitude'],
                dropoff_latitude=row['dropoff_latitude'],
                trip_duration=row['trip_duration']
            )
            models.append(trip)
        return models