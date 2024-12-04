"""Logging configuration and utilities."""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from src.config.settings import Settings

def setup_logging(settings: Settings) -> None:
    """Configure application logging."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create formatters and handlers
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # File handler
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the specified name."""
    return logging.getLogger(name)