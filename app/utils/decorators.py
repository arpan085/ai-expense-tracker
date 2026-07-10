"""
Decorators Module

Provides useful decorators for logging, timing, and error handling.
"""

import time
import functools
from typing import Any, Callable
from app.logger import get_logger

logger = get_logger(__name__)


def timeit(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.

    Args:
        func: Function to measure

    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.debug(
                f"{func.__name__} executed in {execution_time:.4f} seconds"
            )

    return wrapper


def log_function_call(func: Callable) -> Callable:
    """
    Decorator to log function calls.

    Args:
        func: Function to log

    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        logger.info(f"Calling {func.__name__}({signature})")

        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} returned {result!r}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised {type(e).__name__}: {str(e)}")
            raise

    return wrapper


def handle_exceptions(
    default_return: Any = None,
    log_level: str = "error"
) -> Callable:
    """
    Decorator to handle exceptions gracefully.

    Args:
        default_return: Default value to return on exception
        log_level: Logging level

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_func = getattr(logger, log_level)
                log_func(
                    f"Exception in {func.__name__}: {type(e).__name__}: {str(e)}"
                )
                return default_return

        return wrapper

    return decorator


def validate_input(**validators: Callable) -> Callable:
    """
    Decorator to validate function inputs.

    Args:
        **validators: Keyword arguments with validation functions

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Validate kwargs
            for key, validator in validators.items():
                if key in kwargs:
                    if not validator(kwargs[key]):
                        raise ValueError(f"Invalid value for {key}: {kwargs[key]}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """
    Decorator to retry function on exception.

    Args:
        max_attempts: Maximum number of attempts
        delay: Delay between attempts in seconds

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: "
                            f"{str(e)}. Retrying in {delay} seconds..."
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {str(e)}"
                        )
                        raise

        return wrapper

    return decorator


def require_authentication(func: Callable) -> Callable:
    """
    Decorator to require user authentication.

    Args:
        func: Function to decorate

    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs) -> Any:
        if not hasattr(self, 'current_user') or self.current_user is None:
            logger.warning(f"Unauthorized access attempt to {func.__name__}")
            raise PermissionError("Authentication required")

        return func(self, *args, **kwargs)

    return wrapper


def cache_result(duration: int = 300) -> Callable:
    """
    Decorator to cache function results.

    Args:
        duration: Cache duration in seconds

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        cache_time = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_time = time.time()

            # Create cache key from args and kwargs
            cache_key = (args, tuple(sorted(kwargs.items())))

            # Check cache
            if cache_key in cache:
                if current_time - cache_time[cache_key] < duration:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return cache[cache_key]
                else:
                    del cache[cache_key]
                    del cache_time[cache_key]

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache[cache_key] = result
            cache_time[cache_key] = current_time

            logger.debug(f"Result cached for {func.__name__}")
            return result

        return wrapper

    return decorator


def deprecated(message: str = "") -> Callable:
    """
    Decorator to mark functions as deprecated.

    Args:
        message: Deprecation message

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            deprecation_msg = (
                f"{func.__name__} is deprecated. {message}"
                if message
                else f"{func.__name__} is deprecated."
            )
            logger.warning(deprecation_msg)
            return func(*args, **kwargs)

        return wrapper

    return decorator
