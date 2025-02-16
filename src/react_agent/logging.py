"""Logging configuration for the ReAct agent."""

import logging
import sys


def setup_logging(log_level: str = "INFO") -> None:
    """Set up logging configuration.
    
    Args:
        log_level: The logging level to use. Defaults to "INFO".
    """
    # Create formatter for console output
    console_formatter = logging.Formatter(
        "%(levelname)s - %(message)s"
    )

    # Create and configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(getattr(logging, log_level.upper()))

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)

    # Log initial setup
    logging.info("Logging system initialized")


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name.
    
    Args:
        name: The name of the logger, typically __name__
        
    Returns:
        A configured logger instance
    """
    return logging.getLogger(name) 