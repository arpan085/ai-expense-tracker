"""
Input Validation Module

Provides validation functions for user input and data integrity.
"""

import re
from typing import Any, Tuple
from datetime import datetime
from app.exceptions import (
    ValidationException,
    InvalidAmountError,
    InvalidDateError,
    MissingFieldError
)


def validate_username(username: str) -> Tuple[bool, str]:
    """
    Validate username format.

    Args:
        username: Username to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long"

    if len(username) > 20:
        return False, "Username must not exceed 20 characters"

    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"

    return True, ""


def validate_password(password: str, min_length: int = 8) -> Tuple[bool, str]:
    """
    Validate password strength.

    Args:
        password: Password to validate
        min_length: Minimum password length

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        raise MissingFieldError("password")

    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters long"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"

    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format.

    Args:
        email: Email to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        return False, "Invalid email format"

    return True, ""


def validate_amount(amount: Any) -> Tuple[bool, str]:
    """
    Validate expense/income amount.

    Args:
        amount: Amount to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if amount is None or amount == "":
        raise MissingFieldError("amount")

    try:
        amount_float = float(amount)

        if amount_float <= 0:
            return False, "Amount must be greater than 0"

        if amount_float > 1000000:
            return False, "Amount cannot exceed 1,000,000"

        return True, ""

    except (ValueError, TypeError):
        return False, "Amount must be a valid number"


def validate_date(date_str: str) -> Tuple[bool, str]:
    """
    Validate date format (YYYY-MM-DD).

    Args:
        date_str: Date string to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not date_str:
        raise MissingFieldError("date")

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Date must be in YYYY-MM-DD format"


def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
    """
    Validate date range.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if start > end:
            return False, "Start date cannot be after end date"

        return True, ""

    except ValueError:
        return False, "Invalid date format"


def validate_category(category: str, valid_categories: list) -> Tuple[bool, str]:
    """
    Validate category from predefined list.

    Args:
        category: Category to validate
        valid_categories: List of valid categories

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not category:
        raise MissingFieldError("category")

    if category not in valid_categories:
        return False, f"Invalid category. Must be one of: {', '.join(valid_categories)}"

    return True, ""


def validate_description(description: str, max_length: int = 500) -> Tuple[bool, str]:
    """
    Validate description field.

    Args:
        description: Description to validate
        max_length: Maximum allowed length

    Returns:
        Tuple of (is_valid, error_message)
    """
    if description and len(description) > max_length:
        return False, f"Description cannot exceed {max_length} characters"

    return True, ""


def validate_budget_limit(limit: Any) -> Tuple[bool, str]:
    """
    Validate budget limit.

    Args:
        limit: Budget limit to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        limit_float = float(limit)

        if limit_float <= 0:
            return False, "Budget limit must be greater than 0"

        if limit_float > 1000000:
            return False, "Budget limit cannot exceed 1,000,000"

        return True, ""

    except (ValueError, TypeError):
        return False, "Budget limit must be a valid number"


def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input to prevent injection attacks.

    Args:
        user_input: Raw user input

    Returns:
        Sanitized input
    """
    if not isinstance(user_input, str):
        return str(user_input)

    # Remove potentially dangerous characters
    dangerous_chars = ["<", ">", "'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]

    sanitized = user_input
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")

    # Limit length
    sanitized = sanitized[:500]

    return sanitized.strip()


def validate_all(data: dict, required_fields: list) -> Tuple[bool, list]:
    """
    Validate all required fields in data dictionary.

    Args:
        data: Data dictionary to validate
        required_fields: List of required field names

    Returns:
        Tuple of (is_valid, list of missing fields)
    """
    missing_fields = [field for field in required_fields if not data.get(field)]

    return len(missing_fields) == 0, missing_fields
