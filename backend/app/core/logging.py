"""
Structured logging configuration
"""

import logging
import sys
from datetime import datetime
from typing import Dict, Any
import json

class JSONFormatter(logging.Formatter):
    """Format logs as JSON for production"""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)

def setup_logging():
    """Configure application logging"""
    
    # Get log level from settings
    log_level = getattr(logging, "INFO")  # Default
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Use JSON or text format
    if False:  # settings.log_format == "json" (disabled for readability)
        console_handler.setFormatter(JSONFormatter())
    else:
        console_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Reduce noise from libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("transformers").setLevel(logging.WARNING)
    logging.getLogger("torch").setLevel(logging.WARNING)
    
    return root_logger