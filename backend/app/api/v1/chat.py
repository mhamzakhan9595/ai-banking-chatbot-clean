"""
Chat API endpoints - Version 1
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.containers import container
from app.domain.services.chat_service import ChatService
from app.core.exceptions import LLMServiceError
import logging

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])
logger = logging.getLogger(__name__)

def get_chat_service() -> ChatService:
    """Dependency injection for chat service"""
    return container.chat_service

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Send a chat message and get AI response
    """
    try:
        result = await chat_service.process_message(
            message=request.message,
            user_id=request.user_id,
            conversation_id=request.conversation_id
        )
        
        return ChatResponse(
            response=result["response"],
            confidence=result["confidence"],
            from_cache=result.get("from_cache", False),
            conversation_id=result.get("conversation_id"),
            model_used=container.llm_provider.get_info().get("model", "unknown")
        )
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Stream chat response token by token
    """
    async def generate():
        async for chunk in chat_service.stream_message(
            message=request.message,
            user_id=request.user_id
        ):
            yield chunk
    
    return StreamingResponse(generate(), media_type="text/plain")