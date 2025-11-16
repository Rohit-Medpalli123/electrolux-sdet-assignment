"""
Logging utility module using Loguru.

Automatically creates:
- Logs/ folder at project root
- Date-based subfolder: Logs/YYYY-MM-DD/
- Timestamped log file: run_HHMMSS.log

Provides enhanced logging with:
- Color-coded console output
- Automatic log rotation
- Better formatting with milliseconds
- Improved error handling
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from loguru import logger

# Singleton configuration
_initialized: bool = False
_log_file_path: Optional[str] = None


def _get_log_file_path() -> str:
    """
    Create and return the log file path following the project structure.

    Returns:
        Full path to the log file
    """
    # Create Logs directory structure
    project_root = Path(__file__).parent.parent
    logs_dir = project_root / "Logs"
    date_folder = logs_dir / datetime.now().strftime("%Y-%m-%d")
    date_folder.mkdir(parents=True, exist_ok=True)

    # Create timestamped log file
    timestamp = datetime.now().strftime("%H%M%S")
    log_file = date_folder / f"run_{timestamp}.log"

    return str(log_file)


def _initialize_logger():
    """Initialize Loguru logger with custom configuration."""
    global _initialized, _log_file_path

    if _initialized:
        return

    # Get log file path
    _log_file_path = _get_log_file_path()

    # Remove default handler
    logger.remove()

    # Add console handler
    logger.add(
        sink=lambda msg: print(msg, end=""),
        format="<green>{time:YYYY-MM-DD HH:mm:ss,SSS}</green> - {name} - <level>{level}</level> - {message}",
        level="INFO",
    )

    # Add file handler with format matching your desired style
    logger.add(
        sink=_log_file_path,
        format="{time:YYYY-MM-DD HH:mm:ss,SSS} - {name} - {level} - {message}",
        level="DEBUG",
        rotation=None,  # No rotation (one file per run)
        retention=None,  # Keep all files
        encoding="utf-8",
    )

    logger.info(f"Logger initialized. Log file: {_log_file_path}")
    _initialized = True


def get_logger(name: str = "APITestFramework"):
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name for identification in logs

    Returns:
        Loguru logger bound with the specified name
    """
    # Initialize logger on first call
    if not _initialized:
        _initialize_logger()

    # Return logger bound with the name
    return logger.bind(name=name)


def get_log_file_path() -> Optional[str]:
    """
    Get the current log file path.

    Returns:
        Path to the current log file or None if not initialized
    """
    return _log_file_path


def add_execution_separator(log, title: str = "NEW TEST EXECUTION"):
    """
    Add a visual separator in logs for better readability.

    Args:
        log: Logger instance
        title: Title for the separator
    """
    separator = "=" * 80
    log.info(f"\n{separator}\n{title}\n{separator}\n")
