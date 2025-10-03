"""Logging configuration for smart_i2c_motor_driver."""

import logging
import sys
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    stream=None
) -> None:
    """Configure logging for the motor driver library.
    
    Args:
        level: Logging level (default: logging.INFO)
        format_string: Custom format string (optional)
        stream: Output stream (default: sys.stdout)
        
    Example:
        >>> from smart_i2c_motor_driver import setup_logging
        >>> import logging
        >>> setup_logging(level=logging.DEBUG)
    """
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    if stream is None:
        stream = sys.stdout
    
    # Configure root logger for this package
    logger = logging.getLogger("smart_i2c_motor_driver")
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Add console handler
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Prevent propagation to root logger
    logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the package.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"smart_i2c_motor_driver.{name}")
