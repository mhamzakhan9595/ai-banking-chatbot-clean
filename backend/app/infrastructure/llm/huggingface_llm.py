"""
Hugging Face LLM implementation
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, Any, AsyncGenerator
import logging
import asyncio
from app.domain.interfaces.llm_interface import LLMProvider
from app.core.exceptions import LLMServiceError

logger = logging.getLogger(__name__)

class HuggingFaceLLM(LLMProvider):
    """Hugging Face model implementation"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-small"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = self._get_device()
        self._load_model()
    
    def _get_device(self) -> str:
        if torch.cuda.is_available():
            return "cuda"
        return "cpu"
    
    def _load_model(self):
        """Load model and tokenizer"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32 if self.device == "cpu" else torch.float16,
                low_cpu_mem_usage=True
            )
            self.model = self.model.to(self.device)
            self.model.eval()
            logger.info(f"Model loaded on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise LLMServiceError(f"Model loading failed: {e}")
    
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response"""
        if not self.model:
            raise LLMServiceError("Model not loaded")
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=kwargs.get('max_length', 100),
                    temperature=kwargs.get('temperature', 0.7),
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id
                )
            
            response = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            )
            
            return {
                "response": response.strip() or "I'm not sure how to respond.",
                "confidence": min(len(response.split()) / 50, 1.0),
                "model": self.model_name
            }
        except Exception as e:
            logger.error(f"Generation error: {e}")
            raise LLMServiceError(f"Generation failed: {e}")
    
    async def generate_stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Stream response token by token"""
        if not self.model:
            yield "Model not available"
            return
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            input_ids = inputs['input_ids']
            
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_length', 100)
            
            for _ in range(max_tokens):
                with torch.no_grad():
                    outputs = self.model(input_ids)
                    next_token_logits = outputs.logits[0, -1, :] / temperature
                    probs = torch.softmax(next_token_logits, dim=-1)
                    next_token = torch.multinomial(probs, num_samples=1)
                
                token_text = self.tokenizer.decode(next_token, skip_special_tokens=True)
                if token_text and token_text.strip():
                    yield token_text
                
                input_ids = torch.cat([input_ids, next_token.unsqueeze(0)], dim=-1)
                
                if next_token.item() == self.tokenizer.eos_token_id:
                    break
                
                await asyncio.sleep(0.05)
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"Error: {e}"
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "provider": "huggingface",
            "model": self.model_name,
            "device": self.device,
            "loaded": self.model is not None
        }
    
    def is_available(self) -> bool:
        return self.model is not None