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
        
        # Remove suffix from column names if they exist
        df.columns = [col.split('__')[0] for col in df.columns]
        
        # Remove trips with invalid coordinates
        df = df[
            (df['pickup_longitude'] != 0) &
            (df['pickup_latitude'] != 0) &
            (df['dropoff_longitude'] != 0) &
            (df['dropoff_latitude'] != 0)
        ]
        
        # Ensure id column starts with 'id'
        if 'id' in df.columns:
            df['id'] = df['id'].apply(lambda x: f"id{x}" if not str(x).startswith('id') else x)
        
        return df
    
    @staticmethod
    def to_models(df: pd.DataFrame) -> List[TaxiTrip]:
        """Convert DataFrame rows to TaxiTrip models."""
        models = []
        for _, row in df.iterrows():
            trip = TaxiTrip(
                id=row['id'],
                vendor_id=row['vendor_id'],
                pickup_datetime=row['pickup_datetime'],
                passenger_count=row['passenger_count'],
                pickup_longitude=row['pickup_longitude'],
                pickup_latitude=row['pickup_latitude'],
                dropoff_longitude=row['dropoff_longitude'],
                dropoff_latitude=row['dropoff_latitude']
            )
            models.append(trip)
        return models