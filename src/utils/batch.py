"""Batch processing utilities."""
from typing import List, Any, Callable, TypeVar, Iterator

T = TypeVar('T')

class BatchUtils:
    """Utility class for batch processing."""
    
    @staticmethod
    def process_in_batches(
        items: List[T],
        batch_size: int,
        processor: Callable[[List[T]], Any]
    ) -> Iterator[Any]:
        """
        Process items in batches.
        
        Args:
            items: List of items to process
            batch_size: Size of each batch
            processor: Function to process each batch
            
        Yields:
            Any: Result of processing each batch
        """
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            yield processor(batch)
    
    @staticmethod
    def chunk_dataframe(df, chunk_size: int) -> Iterator:
        """
        Split DataFrame into chunks.
        
        Args:
            df: pandas DataFrame
            chunk_size: Size of each chunk
            
        Yields:
            DataFrame: Chunk of the original DataFrame
        """
        for i in range(0, len(df), chunk_size):
            yield df.iloc[i:i + chunk_size]