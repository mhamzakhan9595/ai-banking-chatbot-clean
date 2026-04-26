"""
Health check endpoints - Version 1
"""

from fastapi import APIRouter
from datetime import datetime
from app.core.config import settings
from app.core.containers import container

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """Comprehensive health check"""
    llm_info = None
    llm_status = "unknown"
    
    try:
        if container.llm_provider:
            llm_info = container.llm_provider.get_info()
            llm_status = "loaded" if llm_info.get("loaded") else "error"
    except Exception as e:
        llm_status = f"error: {str(e)}"
    
    return {
        "status": "healthy" if llm_status == "loaded" else "degraded",
        "timestamp": datetime.now().isoformat(),
        "version": settings.app_version,
        "services": {
            "api": "running",
            "llm": llm_status,
            "cache": "enabled" if settings.cache_enabled else "disabled",
            "rate_limiter": "enabled" if settings.rate_limit_enabled else "disabled"
        },
        "model": llm_info
    }