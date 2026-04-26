"""
Chat request/response schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    stream: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What's my account balance?",
                "user_id": "user123"
            }
        }

class ChatResponse(BaseModel):
    response: str
    confidence: float
    from_cache: bool = False
    conversation_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    model_used: str = "unknown"