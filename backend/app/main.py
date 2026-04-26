"""
AI Banking Assistant - Main FastAPI Application
Day 2: Integrated with real Hugging Face LLM
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import logging

# Import our modules
from app.models import ChatRequest, ChatResponse
from app.services import LLMService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="AI Banking Assistant API",
    description="Chatbot with real Hugging Face LLM integration",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM Service (this will load the model)
# This happens once when server starts
logger.info("Starting AI Banking Assistant...")
try:
    llm_service = LLMService(model_name="microsoft/DialoGPT-small")
    logger.info("✓ LLM Service initialized successfully")
except Exception as e:
    logger.error(f"✗ Failed to initialize LLM Service: {e}")
    llm_service = None

# Store conversation histories (in production, use database)
conversations = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    model_status = "loaded" if llm_service and llm_service.is_loaded else "failed"
    return {
        "message": "AI Banking Assistant API is running!",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "llm_status": model_status,
        "model_info": llm_service.get_model_info() if llm_service else None
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "llm": "loaded" if llm_service and llm_service.is_loaded else "not_loaded",
            "database": "not_configured_yet"
        },
        "model_info": llm_service.get_model_info() if llm_service else None
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return AI response
    Uses real Hugging Face model (DialoGPT)
    """
    
    # Validate LLM service is available
    if not llm_service or not llm_service.is_loaded:
        raise HTTPException(
            status_code=503, 
            detail="LLM service is not available. Please try again later."
        )
    
    # Validate input
    if not request.message or len(request.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    logger.info(f"Processing message from user {request.user_id}: {request.message[:50]}...")
    
    try:
        # Get conversation history if user_id provided
        context = None
        if request.user_id:
            if request.user_id not in conversations:
                conversations[request.user_id] = []
            
            # Build context from last 3 exchanges
            if conversations[request.user_id]:
                context = "\n".join(conversations[request.user_id][-6:])  # Last 3 back-and-forth
        
        # Generate response from LLM
        result = llm_service.generate_response(
            user_input=request.message,
            conversation_history=context,
            temperature=0.7,  # Creative but focused
            max_length=150
        )
        
        # Store conversation (if user_id provided)
        if request.user_id:
            conversations[request.user_id].append(f"User: {request.message}")
            conversations[request.user_id].append(f"AI: {result['response']}")
            
            # Keep only last 20 messages to manage memory
            if len(conversations[request.user_id]) > 20:
                conversations[request.user_id] = conversations[request.user_id][-20:]
        
        # Return response
        return ChatResponse(
            response=result['response'],
            confidence=result.get('confidence', 0.5),
            model_used=result.get('model', 'microsoft/DialoGPT-small')
        )
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.get("/model-info")
async def get_model_info():
    """Get information about the loaded model"""
    if not llm_service:
        raise HTTPException(status_code=503, detail="LLM service not available")
    
    return llm_service.get_model_info()

# Run directly (for development)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )









#simple FastAPI app setup with CORS and health check endpoints for testing. This is the starting point for our AI Banking Assistant API, which will later #include LLM integration, RAG, and banking features.
# futher its not needed beause we updated the main.py to include LLM integration and other features. The above code is the complete main.py file with all the necessary imports and endpoints for our AI Banking Assistant API.
# """
# AI Banking Assistant - Main FastAPI Application
# Day 1: Basic server setup
# """

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn
# from datetime import datetime

# # Create FastAPI instance
# app = FastAPI(
#     title="AI Banking Assistant API",
#     description="Chatbot API with LLM, RAG, and banking features",
#     version="1.0.0"
# )

# # Configure CORS (allows frontend to call our API)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, replace with actual frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Root endpoint - test if API is working
# @app.get("/")
# async def root():
#     """Health check endpoint"""
#     return {
#         "message": "AI Banking Assistant API is running!",
#         "status": "active",
#         "timestamp": datetime.now().isoformat(),
#         "version": "1.0.0"
#     }

# # Test endpoint - returns simple response
# @app.get("/health")
# async def health_check():
#     """Detailed health check"""
#     return {
#         "status": "healthy",
#         "services": {
#             "api": "running",
#             "database": "not_configured_yet",
#             "llm": "not_configured_yet"
#         }
#     }

# # Run directly with python (for development)
# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True  # Auto-restart on code changes
#     )