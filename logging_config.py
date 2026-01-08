"""Provides logger"""
import logging
from logging.handlers import RotatingFileHandler

from config import LOG_FILE

def setup_logger():
    """Setup logger with file rotation and defined log format"""
    logger = logging.getLogger("pinboard_archiver")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger  # Prevent duplicate handlers

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
