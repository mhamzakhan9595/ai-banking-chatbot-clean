"""
Global error handling middleware
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import logging
import traceback

from app.core.exceptions import AppException, RateLimitExceededError, LLMServiceError

logger = logging.getLogger(__name__)

def add_error_handlers(app: FastAPI):
    """Register global error handlers"""
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.error(f"App exception: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "detail": exc.message,
                "status_code": exc.status_code
            }
        )
    
    @app.exception_handler(RateLimitExceededError)
    async def rate_limit_handler(request: Request, exc: RateLimitExceededError):
        logger.warning(f"Rate limit exceeded: {request.client.host}")
        return JSONResponse(
            status_code=429,
            content={
                "error": "RateLimitExceeded",
                "detail": exc.message,
                "retry_after": 60
            }
        )
    
    @app.exception_handler(LLMServiceError)
    async def llm_error_handler(request: Request, exc: LLMServiceError):
        logger.error(f"LLM error: {exc.message}")
        return JSONResponse(
            status_code=503,
            content={
                "error": "LLMServiceUnavailable",
                "detail": exc.message,
                "suggestion": "Please try again later"
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Catch-all for unexpected errors"""
        logger.error(f"Unexpected error: {str(exc)}")
        logger.error(traceback.format_exc())
        
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "detail": "An unexpected error occurred",
                "traceback": traceback.format_exc() if app.debug else None
            }
        )