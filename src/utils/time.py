"""Time-related utility functions."""
from datetime import datetime, timedelta
from typing import Optional, Tuple

class TimeUtils:
    """Utility class for time operations."""
    
    @staticmethod
    def parse_datetime(dt_str: str) -> Optional[datetime]:
        """
        Parse datetime string in multiple formats.
        
        Args:
            dt_str: Datetime string
            
        Returns:
            datetime: Parsed datetime object or None if invalid
        """
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(dt_str, fmt)
            except ValueError:
                continue
        return None
    
    @staticmethod
    def get_time_window(
        days: int = 7
    ) -> Tuple[datetime, datetime]:
        """
        Get start and end datetime for a time window.
        
        Args:
            days: Number of days to look back
            
        Returns:
            tuple: (start_datetime, end_datetime)
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return start_date, end_date