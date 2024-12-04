"""Redis cache management."""
from typing import Optional, Any
import json
import redis
from ..config.settings import Settings

class RedisManager:
    """Manages Redis cache operations."""
    
    def __init__(self, settings: Settings):
        self.redis_client = redis.from_url(settings.REDIS_URL or "redis://localhost:6379/0")
        self.ttl = settings.CACHE_TTL
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        self.redis_client.setex(
            key,
            ttl or self.ttl,
            json.dumps(value)
        )
    
    async def delete(self, key: str) -> None:
        """Delete value from cache."""
        self.redis_client.delete(key)
        
    async def clear_all(self) -> None:
        """Clear all cached data."""
        self.redis_client.flushdb()