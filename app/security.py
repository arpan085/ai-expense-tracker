"""
Security Module

Handles password hashing, encryption, and other security operations.
"""

import bcrypt
import secrets
from typing import Tuple
from app.logger import get_logger
from app.config import settings

logger = get_logger(__name__)


class PasswordManager:
    """Manages password hashing and verification using bcrypt."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        try:
            salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
            hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
            return hashed.decode("utf-8")
        except Exception as e:
            logger.error(f"Error hashing password: {str(e)}")
            raise

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            password: Plain text password
            hashed_password: Hashed password to verify against

        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                hashed_password.encode("utf-8")
            )
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False


class TokenManager:
    """Manages security tokens."""

    @staticmethod
    def generate_token(length: int = 32) -> str:
        """
        Generate a secure random token.

        Args:
            length: Token length in bytes

        Returns:
            Hexadecimal token string
        """
        return secrets.token_hex(length)

    @staticmethod
    def generate_session_token() -> str:
        """
        Generate a session token.

        Returns:
            Session token string
        """
        return TokenManager.generate_token(32)

    @staticmethod
    def generate_recovery_token() -> str:
        """
        Generate a password recovery token.

        Returns:
            Recovery token string
        """
        return TokenManager.generate_token(32)


class RateLimiter:
    """
    Simple in-memory rate limiter.
    
    Note: For production, use Redis or similar.
    """

    def __init__(self, max_attempts: int = 5, window_seconds: int = 300):
        """
        Initialize rate limiter.

        Args:
            max_attempts: Maximum attempts allowed
            window_seconds: Time window in seconds
        """
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self.attempts: dict = {}

    def is_rate_limited(self, key: str) -> bool:
        """
        Check if a key is rate limited.

        Args:
            key: Identifier (e.g., username, IP address)

        Returns:
            True if rate limited, False otherwise
        """
        import time

        current_time = time.time()

        if key not in self.attempts:
            self.attempts[key] = []

        # Remove old attempts outside the window
        self.attempts[key] = [
            attempt_time
            for attempt_time in self.attempts[key]
            if current_time - attempt_time < self.window_seconds
        ]

        if len(self.attempts[key]) >= self.max_attempts:
            return True

        self.attempts[key].append(current_time)
        return False

    def reset(self, key: str) -> None:
        """
        Reset rate limit for a key.

        Args:
            key: Identifier to reset
        """
        if key in self.attempts:
            self.attempts[key] = []

    def get_remaining_attempts(self, key: str) -> int:
        """
        Get remaining attempts before rate limit.

        Args:
            key: Identifier

        Returns:
            Number of remaining attempts
        """
        if key not in self.attempts:
            return self.max_attempts

        return max(0, self.max_attempts - len(self.attempts[key]))

    def get_reset_time(self, key: str) -> float:
        """
        Get time until rate limit resets.

        Args:
            key: Identifier

        Returns:
            Seconds until reset
        """
        import time

        if key not in self.attempts or not self.attempts[key]:
            return 0

        oldest_attempt = min(self.attempts[key])
        reset_time = oldest_attempt + self.window_seconds
        return max(0, reset_time - time.time())


class InputSanitizer:
    """Sanitizes user input to prevent injection attacks."""

    @staticmethod
    def sanitize_sql_input(user_input: str) -> str:
        """
        Sanitize input for SQL queries (though SQLAlchemy ORM prevents injection).

        Args:
            user_input: Raw user input

        Returns:
            Sanitized input
        """
        if not isinstance(user_input, str):
            return str(user_input)

        # Remove SQL comments and keywords
        dangerous_patterns = [
            "--",
            "/*",
            "*/",
            "xp_",
            "sp_",
            "UNION",
            "SELECT",
            "INSERT",
            "UPDATE",
            "DELETE",
            "DROP",
        ]

        sanitized = user_input
        for pattern in dangerous_patterns:
            sanitized = sanitized.replace(pattern, "")

        return sanitized.strip()

    @staticmethod
    def sanitize_html_input(user_input: str) -> str:
        """
        Sanitize input for HTML context.

        Args:
            user_input: Raw user input

        Returns:
            HTML-escaped input
        """
        if not isinstance(user_input, str):
            return str(user_input)

        replacements = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#x27;",
        }

        sanitized = user_input
        for char, escape in replacements.items():
            sanitized = sanitized.replace(char, escape)

        return sanitized

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent directory traversal.

        Args:
            filename: Raw filename

        Returns:
            Safe filename
        """
        if not isinstance(filename, str):
            return "file"

        # Remove path separators and dangerous characters
        dangerous_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*", "..", "~"]

        sanitized = filename
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")

        # Limit length
        sanitized = sanitized[:255]

        return sanitized.strip() or "file"


# Global instances
password_manager = PasswordManager()
token_manager = TokenManager()
rate_limiter = RateLimiter(
    max_attempts=settings.MAX_LOGIN_ATTEMPTS,
    window_seconds=300
)
input_sanitizer = InputSanitizer()
