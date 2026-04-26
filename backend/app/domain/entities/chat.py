"""
Domain entities for chat functionality
Business logic lives here, separate from infrastructure
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

@dataclass
class ChatMessage:
    """Individual chat message entity"""
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    confidence: Optional[float] = None
    
    def is_empty(self) -> bool:
        return not self.content or len(self.content.strip()) == 0
    
    def truncate(self, max_length: int = 1000):
        """Truncate message if too long"""
        if len(self.content) > max_length:
            self.content = self.content[:max_length] + "..."

@dataclass
class Conversation:
    """Conversation entity with business logic"""
    conversation_id: str
    user_id: Optional[str] = None
    messages: List[ChatMessage] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    max_history: int = 20
    
    def add_message(self, role: MessageRole, content: str):
        """Add message to conversation"""
        message = ChatMessage(role=role, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now()
        
        # Maintain history limit
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_context(self, last_n: int = 6) -> str:
        """Get formatted context for LLM"""
        recent_messages = self.messages[-last_n:]
        context = ""
        for msg in recent_messages:
            context += f"{msg.role.value}: {msg.content}\n"
        return context
    
    def get_last_message(self) -> Optional[ChatMessage]:
        """Get last message in conversation"""
        return self.messages[-1] if self.messages else None
    
    def clear(self):
        """Clear conversation history"""
        self.messages.clear()
        self.updated_at = datetime.now()