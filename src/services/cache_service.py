"""Service for handling cache operations."""
from typing import Optional, Any, Callable
from functools import wraps
import hashlib
import json
from ..cache.redis_manager import RedisManager
from ..utils.logging import get_logger

logger = get_logger(__name__)

class CacheService:
    """Service for cache operations."""
    
    def __init__(self, redis_manager: RedisManager):
        self.redis = redis_manager
    
    def cached(self, prefix: str, ttl: Optional[int] = None):
        """Decorator for caching function results."""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                key_parts = [prefix, func.__name__]
                key_parts.extend(str(arg) for arg in args)
                key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
                cache_key = hashlib.md5(
                    json.dumps(key_parts).encode()
                ).hexdigest()
                
                # Try to get from cache
                cached_value = await self.redis.get(cache_key)
                if cached_value is not None:
                    logger.debug(f"Cache hit for key: {cache_key}")
                    return cached_value
                
                # Execute function and cache result
                result = await func(*args, **kwargs)
                await self.redis.set(cache_key, result, ttl)
                logger.debug(f"Cached result for key: {cache_key}")
                return result
            return wrapper
        return decorator