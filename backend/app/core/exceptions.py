"""
Custom exceptions for better error handling
"""

class AppException(Exception):
    """Base exception for application"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class LLMServiceError(AppException):
    """LLM service related errors"""
    def __init__(self, message: str):
        super().__init__(message, status_code=503)

class RateLimitExceededError(AppException):
    """Rate limit exceeded"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)

class ModelNotFoundError(AppException):
    """Model not found"""
    def __init__(self, model_name: str):
        super().__init__(f"Model '{model_name}' not found", status_code=404)

class CacheError(AppException):
    """Cache operation failed"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)

class ValidationError(AppException):
    """Input validation failed"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)