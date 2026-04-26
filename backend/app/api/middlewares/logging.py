"""
Request/Response logging middleware
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and their processing time"""
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = f"{datetime.now().timestamp()}-{id(request)}"
        
        # Log request
        logger.info(f"REQUEST [{request_id}] {request.method} {request.url.path}")
        
        # Record start time
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = (time.time() - start_time) * 1000  # milliseconds
            
            # Log response
            logger.info(
                f"RESPONSE [{request_id}] {response.status_code} | "
                f"Duration: {duration:.2f}ms"
            )
            
            # Add timing header
            response.headers["X-Response-Time"] = f"{duration:.2f}ms"
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            # Log error
            duration = (time.time() - start_time) * 1000
            logger.error(
                f"ERROR [{request_id}] {str(e)} | "
                f"Duration: {duration:.2f}ms"
            )
            raise