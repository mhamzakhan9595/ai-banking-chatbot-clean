"""
LLM Service - Handles all AI model operations
Day 2: Basic Hugging Face integration
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """Service class for managing LLM operations"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-small"):
        """
        Initialize the LLM service with a specific model
        
        Args:
            model_name: Hugging Face model identifier
                       Options: 
                       - "microsoft/DialoGPT-small" (fastest, 124M params)
                       - "microsoft/DialoGPT-medium" (better, 355M params)  
                       - "microsoft/DialoGPT-large" (best, 762M params, needs more RAM)
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = self._get_device()
        self.is_loaded = False
        
        logger.info(f"Initializing LLM Service with model: {model_name}")
        logger.info(f"Using device: {self.device}")
        
        # Load model immediately
        self._load_model()
    
    def _get_device(self) -> str:
        """
        Determine best available device (GPU > CPU)
        Windows with CUDA? Use GPU. Otherwise CPU.
        """
        if torch.cuda.is_available():
            logger.info("CUDA (GPU) detected - using GPU acceleration")
            return "cuda"
        elif torch.backends.mps.is_available():
            logger.info("MPS detected - using Apple Silicon GPU")
            return "mps"
        else:
            logger.info("No GPU detected - using CPU (slower but works)")
            return "cpu"
    
    def _load_model(self):
        """Load the model and tokenizer from Hugging Face"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            logger.info("First download may take 2-5 minutes (downloading ~500MB)...")
            
            # Load tokenizer (converts text to numbers)
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                padding_side='left'
            )
            
            # Add padding token if missing
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32 if self.device == "cpu" else torch.float16,
                low_cpu_mem_usage=True
            )
            
            # Move model to device (GPU/CPU)
            self.model = self.model.to(self.device)
            
            # Set to evaluation mode
            self.model.eval()
            
            self.is_loaded = True
            logger.info(f"✓ Model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self.is_loaded = False
            raise RuntimeError(f"Could not load LLM model: {e}")
    
    def generate_response(
        self, 
        user_input: str, 
        conversation_history: Optional[str] = None,
        max_length: int = 100,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> Dict[str, Any]:
        """
        Generate a response from the model
        
        Args:
            user_input: User's message
            conversation_history: Previous conversation context
            max_length: Maximum response length in tokens
            temperature: Randomness (0=deterministic, 1=creative)
            top_p: Nucleus sampling parameter
        
        Returns:
            Dictionary with response and metadata
        """
        if not self.is_loaded:
            return {
                "response": "I'm still initializing. Please wait a moment...",
                "error": "Model not loaded"
            }
        
        try:
            # Prepare input with context
            if conversation_history:
                full_prompt = f"{conversation_history}User: {user_input}\nAI:"
            else:
                full_prompt = f"User: {user_input}\nAI:"
            
            # Tokenize input
            inputs = self.tokenizer(
                full_prompt, 
                return_tensors="pt",
                truncation=True,
                max_length=512
            )
            
            # Move to same device as model
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate response
            with torch.no_grad():  # Disable gradient calculation (faster)
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode the generated text
            response = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:], 
                skip_special_tokens=True
            )
            
            # Clean up response
            response = response.strip()
            
            # If empty response, provide fallback
            if not response:
                response = "I'm not sure how to respond to that. Could you rephrase?"
            
            # Calculate confidence (basic version)
            confidence = min(len(response.split()) / 50, 1.0) if response else 0.0
            
            return {
                "response": response,
                "confidence": confidence,
                "tokens_used": outputs.shape[1],
                "model": self.model_name
            }
            
        except Exception as e:
            logger.error(f"Generation error: {str(e)}")
            return {
                "response": "I encountered an error processing your request.",
                "error": str(e),
                "model": self.model_name
            }
    
    def reload_model(self, model_name: str):
        """Switch to a different model"""
        self.model_name = model_name
        self._load_model()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about current model"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "is_loaded": self.is_loaded,
            "model_size": "124M parameters" if "small" in self.model_name else "Unknown"
        }