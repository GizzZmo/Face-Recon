"""
Error handling utilities for Face-Recon system.

Provides error logging and safe function execution wrappers.
"""

import functools
import logging
import traceback
from typing import Any, Callable


def setup_logger(log_file: str = "error.log") -> logging.Logger:
    """
    Set up error logger.

    Args:
        log_file: Path to log file

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("face_recon")
    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)
    return logger


def log_error(exc: Exception, log_file: str = "error.log") -> None:
    """
    Log an exception with full traceback.

    Args:
        exc: Exception to log
        log_file: Path to log file (default: error.log)
    """
    logger = setup_logger(log_file)
    logger.error(f"Error: {exc}\n{traceback.format_exc()}")
    print(f"Error logged: {exc}")


def safe_run(func: Callable) -> Callable:
    """
    Decorator to safely execute functions with error logging.

    Args:
        func: Function to wrap

    Returns:
        Wrapped function that logs errors instead of crashing

    Example:
        @safe_run
        def risky_operation():
            # code that might fail
            pass
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_error(e)
            return None

    return wrapper


# Example usage
if __name__ == "__main__":

    @safe_run
    def test_function():
        """Test function that raises an error."""
        raise ValueError("Test error")

    # This will log the error instead of crashing
    test_function()
    print("Program continues after error")
