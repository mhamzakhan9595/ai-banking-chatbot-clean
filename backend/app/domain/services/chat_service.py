"""
Chat service - core business logic for chat operations
"""

import logging
from typing import Optional, Dict, Any, AsyncGenerator
from app.domain.entities.chat import Conversation, MessageRole
from app.domain.interfaces.llm_interface import LLMProvider
from app.domain.interfaces.cache_interface import CacheProvider
from app.domain.interfaces.rate_limit_interface import RateLimiter
from app.core.exceptions import LLMServiceError

logger = logging.getLogger(__name__)

class ChatService:
    """Service handling chat business logic"""
    
    def __init__(
        self,
        llm_provider: LLMProvider,
        cache_provider: Optional[CacheProvider] = None,
        rate_limiter: Optional[RateLimiter] = None
    ):
        self.llm = llm_provider
        self.cache = cache_provider
        self.rate_limiter = rate_limiter
        self.conversations: Dict[str, Conversation] = {}
    
    async def process_message(
        self,
        message: str,
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Process a user message and return AI response
        """
        # Validate input
        if not message or len(message.strip()) == 0:
            raise ValueError("Message cannot be empty")
        
        # Rate limiting
        if self.rate_limiter and user_id:
            allowed, wait_time = await self.rate_limiter.is_allowed(user_id)
            if not allowed:
                raise Exception(f"Rate limit exceeded. Wait {wait_time}s")
        
        # Check cache
        cache_key = f"chat:{user_id}:{message.lower().strip()}"
        if use_cache and self.cache:
            cached_response = await self.cache.get(cache_key)
            if cached_response:
                logger.info(f"Cache hit for message: {message[:50]}")
                return {
                    "response": cached_response,
                    "from_cache": True,
                    "confidence": 0.95
                }
        
        # Get or create conversation
        conv_id = conversation_id or user_id or "default"
        if conv_id not in self.conversations:
            self.conversations[conv_id] = Conversation(
                conversation_id=conv_id,
                user_id=user_id
            )
        
        conversation = self.conversations[conv_id]
        
        # Add user message
        conversation.add_message(MessageRole.USER, message)
        
        # Get context
        context = conversation.get_context(last_n=6)
        
        # Generate response from LLM
        try:
            # Build prompt with context
            prompt = f"{context}User: {message}\nAssistant:"
            
            llm_result = await self.llm.generate(
                prompt=prompt,
                temperature=0.7,
                max_length=150
            )
            
            response_text = llm_result.get("response", "I couldn't generate a response.")
            
            # Add assistant response to conversation
            conversation.add_message(MessageRole.ASSISTANT, response_text)
            
            # Cache response
            if use_cache and self.cache:
                await self.cache.set(cache_key, response_text, ttl=300)
            
            return {
                "response": response_text,
                "from_cache": False,
                "confidence": llm_result.get("confidence", 0.5),
                "conversation_id": conv_id
            }
            
        except Exception as e:
            logger.error(f"LLM generation failed: {str(e)}")
            raise LLMServiceError(f"Failed to generate response: {str(e)}")
    
    async def stream_message(
        self,
        message: str,
        user_id: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Stream response token by token"""
        conversation_id = user_id or "default"
        
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = Conversation(
                conversation_id=conversation_id,
                user_id=user_id
            )
        
        conversation = self.conversations[conversation_id]
        conversation.add_message(MessageRole.USER, message)
        
        context = conversation.get_context(last_n=6)
        prompt = f"{context}User: {message}\nAssistant:"
        full_response = ""
        
        async for chunk in self.llm.generate_stream(
            prompt=prompt,
            temperature=0.7
        ):
            full_response += chunk
            yield chunk
        
        conversation.add_message(MessageRole.ASSISTANT, full_response)
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        return self.conversations.get(conversation_id)
    
    def clear_conversation(self, conversation_id: str):
        """Clear conversation history"""
        if conversation_id in self.conversations:
            self.conversations[conversation_id].clear()