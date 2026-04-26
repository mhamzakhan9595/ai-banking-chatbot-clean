"""
Dependency Injection Container
Manages application dependencies
"""

from app.domain.services.chat_service import ChatService
# Comment out for now - will implement later
# from app.domain.services.model_service import ModelService
from app.infrastructure.llm.model_factory import LLMFactory
from app.infrastructure.cache.memory_cache import MemoryCache
from app.infrastructure.rate_limit.memory_limiter import MemoryRateLimiter
from app.core.config import settings

class Container:
    """Application dependency container"""
    
    def __init__(self):
        self._cache = None
        self._rate_limiter = None
        self._llm_provider = None
        self._chat_service = None
    
    @property
    def cache(self):
        """Get cache provider"""
        if not self._cache:
            self._cache = MemoryCache(
                max_size=settings.cache_max_size,
                ttl=settings.cache_ttl
            )
        return self._cache
    
    @property
    def rate_limiter(self):
        """Get rate limiter"""
        from app.infrastructure.rate_limit.memory_limiter import MemoryRateLimiter
        if not self._rate_limiter:
            self._rate_limiter = MemoryRateLimiter(
                requests_per_minute=settings.rate_limit_requests
            )
        return self._rate_limiter
    
    @property
    def llm_provider(self):
        """Get LLM provider"""
        if not self._llm_provider:
            self._llm_provider = LLMFactory.create(
                model_type="huggingface",
                model_name=settings.model_name
            )
        return self._llm_provider
    
    @property
    def chat_service(self):
        """Get chat service"""
        if not self._chat_service:
            self._chat_service = ChatService(
                llm_provider=self.llm_provider,
                cache_provider=self.cache,
                rate_limiter=self.rate_limiter
            )
        return self._chat_service

# Global container instance
container = Container()