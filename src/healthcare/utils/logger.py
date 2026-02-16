"""Shared logging helpers for the application."""

import logging
import sys

from healthcare.config.settings import Settings


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Configure and return a logger instance with consistent formatting.

    Args:
        name: Logger name (typically __name__)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers
    if logger.handlers:
        return logger

    # Set log level from settings
    logger.setLevel(getattr(logging, Settings.LOG_LEVEL))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, Settings.LOG_LEVEL))

    # Formatter
    formatter = logging.Formatter(Settings.LOG_FORMAT)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Get a configured logger for the given module or component name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        logging.Logger: Logger instance
    """
    # Ensure callers always receive a configured logger.
    return setup_logger(name)
