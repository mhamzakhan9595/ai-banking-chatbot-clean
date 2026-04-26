"""
Common Pydantic schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    services: dict

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.now)

class SuccessResponse(BaseModel):
    message: str
    data: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.now)