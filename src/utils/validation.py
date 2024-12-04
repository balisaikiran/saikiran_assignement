"""Validation utilities for the TaxiTripDataService."""
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import HTTPException

class ValidationUtils:
    """Utility class for input validation."""
    
    @staticmethod
    def validate_date_range(
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> None:
        """
        Validate date range parameters.
        
        Args:
            start_date: Start date of the range
            end_date: End date of the range
            
        Raises:
            HTTPException: If date range is invalid
        """
        if start_date and end_date and start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="Start date must be before end date"
            )
    
    @staticmethod
    def validate_coordinates(coords: Dict[str, Any]) -> None:
        """
        Validate geographical coordinates.
        
        Args:
            coords: Dictionary containing latitude and longitude
            
        Raises:
            HTTPException: If coordinates are invalid
        """
        if not (-90 <= coords.get('latitude', 0) <= 90):
            raise HTTPException(
                status_code=400,
                detail="Invalid latitude value"
            )
        if not (-180 <= coords.get('longitude', 0) <= 180):
            raise HTTPException(
                status_code=400,
                detail="Invalid longitude value"
            )