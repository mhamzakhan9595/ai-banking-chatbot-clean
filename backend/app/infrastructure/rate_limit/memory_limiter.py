"""
In-memory rate limiter implementation
"""

from typing import Dict, Tuple, List
import time
from collections import defaultdict
import logging
from app.domain.interfaces.rate_limit_interface import RateLimiter

logger = logging.getLogger(__name__)

class MemoryRateLimiter(RateLimiter):
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests_per_minute: int = 10):
        """
        Initialize rate limiter
        
        Args:
            requests_per_minute: Maximum requests allowed per minute
        """
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[float]] = defaultdict(list)
    
    async def is_allowed(self, key: str) -> Tuple[bool, int]:
        """
        Check if request is allowed
        
        Returns:
            (allowed, seconds_to_wait)
        """
        current_time = time.time()
        window_start = current_time - 60
        
        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[key]) >= self.requests_per_minute:
            oldest_request = min(self.requests[key])
            wait_time = int(60 - (current_time - oldest_request))
            logger.warning(f"Rate limit exceeded for {key}, wait {wait_time}s")
            return False, wait_time
        
        # Allow request
        self.requests[key].append(current_time)
        return True, 0
    
    async def get_remaining(self, key: str) -> int:
        """Get remaining requests for key"""
        current_time = time.time()
        window_start = current_time - 60
        
        recent_requests = [
            req_time for req_time in self.requests[key]
            if req_time > window_start
        ]
        
        return max(0, self.requests_per_minute - len(recent_requests))
    
    async def reset(self, key: str):
        """Reset rate limit for key"""
        self.requests[key] = []
        logger.info(f"Rate limit reset for {key}")