"""RESTful API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database.models import TaxiTrip
from ..services.trip_service import TripService
from ..data.ingestion import DataIngestionService
from ..utils.validation import ValidationUtils
import pandas as pd
from ..database.session import get_db
import os

router = APIRouter()

@router.get("/trips/")
async def get_trips(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get taxi trips within a date range."""
    ValidationUtils.validate_date_range(start_date, end_date)
    service = TripService(db)
    return service.get_trips(start_date, end_date, limit)

@router.get("/trips/stats")
async def get_trip_stats(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get statistical information about trips."""
    ValidationUtils.validate_date_range(start_date, end_date)
    service = TripService(db)
    return service.get_trip_stats(start_date, end_date)

@router.get("/trips/process")
async def process_trip_data(
    batch_size: int = 1000,
    db: Session = Depends(get_db)
):
    """Process taxi trip data from the dataset."""
    try:
        # Use Docker container path
        file_path = "/app/data/test.csv"
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail=f"Dataset not found at: {file_path}"
            )

        # Initialize service and process file
        ingestion_service = DataIngestionService(db)
        
        try:
            # Verify file can be read
            pd.read_csv(file_path, nrows=1)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error reading CSV file: {str(e)}"
            )

        try:
            stats = ingestion_service.ingest_csv(file_path, batch_size)
            return {
                "message": "Data processing completed successfully",
                "statistics": stats
            }
        except Exception as e:
            # Log the full error for debugging
            import traceback
            print(f"Data ingestion error: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Error during data ingestion: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )