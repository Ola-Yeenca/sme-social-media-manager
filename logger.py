#!/usr/bin/env python3
"""
Logging infrastructure for SME Social Media Manager
Provides structured logging with console and file output
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


class BotLogger:
    """Centralized logging for the social media bot"""

    _loggers = {}

    @staticmethod
    def setup_logger(name: str, level: str = "INFO", log_to_file: bool = True) -> logging.Logger:
        """
        Configure structured logging for the bot

        Args:
            name: Logger name (usually module name)
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file: Whether to log to file in addition to console

        Returns:
            Configured logger instance

        Example:
            >>> logger = BotLogger.setup_logger(__name__)
            >>> logger.info("Bot started successfully")
        """
        # Return existing logger if already configured
        if name in BotLogger._loggers:
            return BotLogger._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        logger.propagate = False  # Prevent duplicate logs

        # Clear any existing handlers
        logger.handlers.clear()

        # Console handler with color-coded formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        # Detailed format for console
        console_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File handler with rotation (if enabled)
        if log_to_file:
            # Create logs directory if it doesn't exist
            log_dir = Path(__file__).parent / 'logs'
            log_dir.mkdir(exist_ok=True)

            # General log file (all levels)
            log_file = log_dir / f'bot_{datetime.now().strftime("%Y%m%d")}.log'
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.INFO)
            file_formatter = logging.Formatter(
                '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

            # Error log file (errors only)
            error_log_file = log_dir / 'bot_errors.log'
            error_handler = RotatingFileHandler(
                error_log_file,
                maxBytes=5 * 1024 * 1024,  # 5MB
                backupCount=3
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(file_formatter)
            logger.addHandler(error_handler)

        # Cache logger
        BotLogger._loggers[name] = logger

        return logger

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get an existing logger or create a new one with default settings

        Args:
            name: Logger name

        Returns:
            Logger instance
        """
        if name in BotLogger._loggers:
            return BotLogger._loggers[name]
        return BotLogger.setup_logger(name)


# Convenience function for quick logger access
def get_logger(name: str = __name__, level: str = "INFO") -> logging.Logger:
    """
    Quick access to configured logger

    Args:
        name: Logger name (defaults to calling module)
        level: Logging level

    Returns:
        Configured logger instance
    """
    return BotLogger.setup_logger(name, level)


# Example usage and testing
if __name__ == "__main__":
    # Test logger
    logger = get_logger("test_logger")

    logger.debug("This is a debug message")
    logger.info("✅ Bot initialized successfully")
    logger.warning("⚠️ API rate limit approaching")
    logger.error("❌ Failed to post content")
    logger.critical("🚨 System failure - shutting down")

    print("\n✅ Logger test completed - check logs/ directory for files")
