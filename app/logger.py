"""
Logging Configuration Module

Sets up comprehensive logging for the application with both file and console handlers.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from app.config import settings


def setup_logger(
    name: str,
    level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Setup and configure a logger instance.

    Args:
        name: Logger name (typically __name__)
        level: Logging level (defaults to settings.LOG_LEVEL)
        log_file: Path to log file (defaults to settings.LOG_FILE)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Set logging level
    log_level = getattr(logging, level or settings.LOG_LEVEL, logging.INFO)
    logger.setLevel(log_level)

    # Create formatters
    formatter = logging.Formatter(settings.LOG_FORMAT)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    if log_file or settings.LOG_FILE:
        log_path = Path(log_file or settings.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            str(log_path),
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with the given name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Root logger setup
root_logger = setup_logger("ai_expense_tracker")
