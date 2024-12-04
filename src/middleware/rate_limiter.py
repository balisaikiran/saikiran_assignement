"""Rate limiting middleware."""
from typing import Dict, Optional
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from ..cache.redis_manager import RedisManager

class RateLimiter:
    """Rate limiting implementation."""
    
    def __init__(self, redis_manager: RedisManager, requests_per_minute: int = 60):
        self.redis = redis_manager
        self.requests_per_minute = requests_per_minute
    
    async def check_rate_limit(self, request: Request) -> None:
        """Check if request is within rate limits."""
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        # Get current count
        count = await self.redis.get(key) or 0
        
        if count >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
        
        # Increment count
        await self.redis.set(key, count + 1, ttl=60)  # Reset after 1 minute