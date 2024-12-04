"""Data ingestion functionality for taxi trip data."""
import pandas as pd
from typing import List
from pathlib import Path
from sqlalchemy.orm import Session
from .processor import DataProcessor
from ..database.models import TaxiTrip

class DataIngestionService:
    """Service for handling data ingestion operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.processor = DataProcessor()
    
    def ingest_csv(self, file_path: str, batch_size: int = 1000) -> dict:
        """
        Ingest data from CSV file in batches.
        
        Args:
            file_path: Path to the CSV file
            batch_size: Number of records to process in each batch
            
        Returns:
            dict: Statistics about the ingestion process
        """
        if not Path(file_path).exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
            
        stats = {
            "total_records": 0,
            "processed_records": 0,
            "failed_records": 0
        }
        
        # Read CSV in chunks
        for chunk in pd.read_csv(file_path, chunksize=batch_size):
            try:
                # Clean data
                cleaned_chunk = self.processor.clean_data(chunk)
                
                # Convert to models
                models = self.processor.to_models(cleaned_chunk)
                
                # Bulk insert
                self.db.bulk_save_objects(models)
                self.db.commit()
                
                stats["processed_records"] += len(models)
                stats["failed_records"] += len(chunk) - len(models)
                
            except Exception as e:
                self.db.rollback()
                stats["failed_records"] += len(chunk)
                print(f"Error processing batch: {str(e)}")
                
            stats["total_records"] += len(chunk)
            
        return stats