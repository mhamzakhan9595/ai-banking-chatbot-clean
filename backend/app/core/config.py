"""
Application configuration management
Loads from .env file with defaults
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # App info
    app_name: str = "AI Banking Assistant"
    app_version: str = "3.0.0"
    debug: bool = True
    
    # Server
    api_port: int = 8000
    host: str = "0.0.0.0"
    
    # LLM Configuration
    model_name: str = "microsoft/DialoGPT-small"
    fallback_model: str = "microsoft/DialoGPT-small"
    max_response_length: int = 150
    temperature: float = 0.7
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 10  # requests per minute
    rate_limit_window: int = 60    # seconds
    
    # Caching
    cache_enabled: bool = True
    cache_ttl: int = 300  # seconds (5 minutes)
    cache_max_size: int = 100  # max items in cache
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # json or text
    
    # Redis (optional - if not available, uses memory cache)
    redis_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings()