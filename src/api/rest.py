"""RESTful API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database.models import TaxiTrip
from ..services.trip_service import TripService
from ..data.ingestion import DataIngestionService
from ..utils.validation import ValidationUtils

router = APIRouter()

@router.get("/trips/")
async def get_trips(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    db: Session = Depends(lambda: None)  # Replace with actual dependency
):
    """Get taxi trips within a date range."""
    ValidationUtils.validate_date_range(start_date, end_date)
    service = TripService(db)
    return service.get_trips(start_date, end_date, limit)

@router.get("/trips/stats")
async def get_trip_stats(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(lambda: None)  # Replace with actual dependency
):
    """Get statistical information about trips."""
    ValidationUtils.validate_date_range(start_date, end_date)
    service = TripService(db)
    return service.get_trip_stats(start_date, end_date)

@router.post("/trips/upload")
async def upload_trip_data(
    file: UploadFile = File(...),
    batch_size: int = 1000,
    db: Session = Depends(lambda: None)  # Replace with actual dependency
):
    """Upload and process taxi trip data from CSV."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported"
        )
    
    ingestion_service = DataIngestionService(db)
    
    # Save uploaded file temporarily
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        stats = ingestion_service.ingest_csv(temp_path, batch_size)
        return {
            "message": "Data ingestion completed successfully",
            "statistics": stats
        }
    finally:
        import os
        os.remove(temp_path)