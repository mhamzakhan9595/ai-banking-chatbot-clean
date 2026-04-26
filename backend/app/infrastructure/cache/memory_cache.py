"""
In-memory cache implementation using TTLCache
"""

from typing import Dict, Any, Optional
from cachetools import TTLCache
import logging
from app.domain.interfaces.cache_interface import CacheProvider

logger = logging.getLogger(__name__)

class MemoryCache(CacheProvider):
    """TTL-based in-memory cache implementation"""
    
    def __init__(self, max_size: int = 100, ttl: int = 300):
        """
        Initialize memory cache
        
        Args:
            max_size: Maximum number of items in cache
            ttl: Time to live in seconds
        """
        self.cache = TTLCache(maxsize=max_size, ttl=ttl)
        self.hits = 0
        self.misses = 0
        self.max_size = max_size
        self.ttl = ttl
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            self.hits += 1
            logger.debug(f"Cache HIT: {key}")
            return self.cache[key]
        
        self.misses += 1
        logger.debug(f"Cache MISS: {key}")
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        self.cache[key] = value
        logger.debug(f"Cache SET: {key}")
    
    async def delete(self, key: str):
        """Delete from cache"""
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache DELETE: {key}")
    
    async def clear(self):
        """Clear entire cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl_seconds": self.ttl,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2%}"
        }