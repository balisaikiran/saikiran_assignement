"""Geographical utilities and calculations."""
from math import radians, sin, cos, sqrt, atan2
from typing import Tuple, Dict

class GeoUtils:
    """Utility class for geographical calculations."""
    
    EARTH_RADIUS_KM = 6371.0
    
    @staticmethod
    def calculate_distance(
        point1: Tuple[float, float],
        point2: Tuple[float, float]
    ) -> float:
        """
        Calculate distance between two points using Haversine formula.
        
        Args:
            point1: Tuple of (latitude, longitude) for first point
            point2: Tuple of (latitude, longitude) for second point
            
        Returns:
            float: Distance in kilometers
        """
        lat1, lon1 = map(radians, point1)
        lat2, lon2 = map(radians, point2)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return GeoUtils.EARTH_RADIUS_KM * c
    
    @staticmethod
    def is_valid_coordinates(coords: Dict[str, float]) -> bool:
        """
        Validate geographical coordinates.
        
        Args:
            coords: Dictionary with 'latitude' and 'longitude' keys
            
        Returns:
            bool: True if coordinates are valid
        """
        lat = coords.get('latitude', 0)
        lon = coords.get('longitude', 0)
        return -90 <= lat <= 90 and -180 <= lon <= 180