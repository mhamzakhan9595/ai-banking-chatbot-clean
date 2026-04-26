"""
Chat data models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=1000, description="User's input message")
    user_id: Optional[str] = Field(None, description="User identifier for session")
    conversation_id: Optional[str] = Field(None, description="Track conversation history")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What's my account balance?",
                "user_id": "user123"
            }
        }

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="AI generated response")
    confidence: Optional[float] = Field(None, description="Response confidence score")
    timestamp: datetime = Field(default_factory=datetime.now)
    model_used: str = Field(..., description="Which model generated response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Your current account balance is $5,247.89",
                "confidence": 0.92,
                "timestamp": "2024-01-15T10:30:00",
                "model_used": "microsoft/DialoGPT-small"
            }
        }

class ConversationHistory(BaseModel):
    """Store conversation context"""
    messages: List[Dict[str, str]] = []
    max_length: int = 10  # Keep last 10 exchanges
    
    def add_message(self, role: str, content: str):
        """Add message to history"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent messages
        if len(self.messages) > self.max_length:
            self.messages = self.messages[-self.max_length:]
    
    def get_context(self) -> str:
        """Convert history to context string for LLM"""
        context = ""
        for msg in self.messages[-5:]:  # Last 5 messages
            context += f"{msg['role']}: {msg['content']}\n"
        return context