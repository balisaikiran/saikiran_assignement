"""Metrics and statistics utilities."""
from typing import List, Dict, Any
import numpy as np
from statistics import mean, median, stdev

class MetricsUtils:
    """Utility class for statistical calculations."""
    
    @staticmethod
    def calculate_basic_stats(values: List[float]) -> Dict[str, float]:
        """
        Calculate basic statistical measures.
        
        Args:
            values: List of numerical values
            
        Returns:
            dict: Statistical measures
        """
        if not values:
            return {
                "count": 0,
                "mean": 0,
                "median": 0,
                "std": 0,
                "min": 0,
                "max": 0
            }
            
        return {
            "count": len(values),
            "mean": mean(values),
            "median": median(values),
            "std": stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values)
        }
    
    @staticmethod
    def calculate_percentiles(
        values: List[float],
        percentiles: List[float] = [25, 50, 75, 90, 95, 99]
    ) -> Dict[str, float]:
        """
        Calculate percentiles for a list of values.
        
        Args:
            values: List of numerical values
            percentiles: List of percentiles to calculate
            
        Returns:
            dict: Percentile values
        """
        if not values:
            return {f"p{p}": 0 for p in percentiles}
            
        results = np.percentile(values, percentiles)
        return {f"p{p}": v for p, v in zip(percentiles, results)}