"""
Authentication Module

Handles user authentication, registration, and session management.
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from app.models import User
from app.security import password_manager, rate_limiter
from app.logger import get_logger
from app.exceptions import (
    UserNotFoundError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    AuthenticationException,
)

logger = get_logger(__name__)


class AuthService:
    """Authentication service for user management."""

    def __init__(self, session: Session):
        """
        Initialize auth service.

        Args:
            session: SQLAlchemy database session
        """
        self.session = session

    def register(
        self,
        username: str,
        email: str,
        password: str
    ) -> Tuple[bool, str]:
        """
        Register a new user.

        Args:
            username: Username
            email: Email address
            password: Plain text password

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Check if user already exists
            existing_user = self.session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()

            if existing_user:
                if existing_user.username == username:
                    logger.warning(f"Registration failed: Username '{username}' already exists")
                    raise UserAlreadyExistsError(username)
                else:
                    logger.warning(f"Registration failed: Email '{email}' already registered")
                    raise UserAlreadyExistsError(username)

            # Hash password
            password_hash = password_manager.hash_password(password)

            # Create new user
            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                is_active=True,
                theme_preference="dark",
                language="en",
            )

            self.session.add(new_user)
            self.session.commit()

            logger.info(f"User registered successfully: {username}")
            return True, "Registration successful"

        except UserAlreadyExistsError:
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"Registration error: {str(e)}")
            raise AuthenticationException(f"Registration failed: {str(e)}")

    def login(self, username: str, password: str) -> Tuple[bool, Optional[User]]:
        """
        Authenticate user login.

        Args:
            username: Username
            password: Plain text password

        Returns:
            Tuple of (success: bool, user: User or None)
        """
        try:
            # Check rate limiting
            if rate_limiter.is_rate_limited(username):
                logger.warning(f"Login rate limit exceeded for: {username}")
                raise InvalidCredentialsError(
                    "Too many login attempts. Please try again later."
                )

            # Find user
            user = self.session.query(User).filter_by(username=username).first()

            if not user:
                logger.warning(f"Login failed: User not found - {username}")
                raise UserNotFoundError(username)

            # Check if user is active
            if not user.is_active:
                logger.warning(f"Login failed: User inactive - {username}")
                raise InvalidCredentialsError("User account is inactive")

            # Verify password
            if not password_manager.verify_password(password, user.password_hash):
                logger.warning(f"Login failed: Invalid password - {username}")
                raise InvalidCredentialsError("Invalid username or password")

            # Update last login
            user.last_login = datetime.utcnow()
            self.session.commit()

            # Reset rate limiter on successful login
            rate_limiter.reset(username)

            logger.info(f"User logged in successfully: {username}")
            return True, user

        except (UserNotFoundError, InvalidCredentialsError):
            raise
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            raise AuthenticationException(f"Login failed: {str(e)}")

    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> Tuple[bool, str]:
        """
        Change user password.

        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Find user
            user = self.session.query(User).filter_by(id=user_id).first()

            if not user:
                raise UserNotFoundError("User not found")

            # Verify old password
            if not password_manager.verify_password(old_password, user.password_hash):
                raise InvalidCredentialsError("Current password is incorrect")

            # Update password
            user.password_hash = password_manager.hash_password(new_password)
            user.updated_at = datetime.utcnow()
            self.session.commit()

            logger.info(f"Password changed for user: {user_id}")
            return True, "Password changed successfully"

        except Exception as e:
            self.session.rollback()
            logger.error(f"Password change error: {str(e)}")
            raise AuthenticationException(f"Password change failed: {str(e)}")

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User object or None
        """
        try:
            user = self.session.query(User).filter_by(id=user_id).first()
            return user
        except Exception as e:
            logger.error(f"Error retrieving user: {str(e)}")
            return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username: Username

        Returns:
            User object or None
        """
        try:
            user = self.session.query(User).filter_by(username=username).first()
            return user
        except Exception as e:
            logger.error(f"Error retrieving user: {str(e)}")
            return None

    def update_user_settings(
        self,
        user_id: int,
        settings: dict
    ) -> Tuple[bool, str]:
        """
        Update user settings.

        Args:
            user_id: User ID
            settings: Dictionary of settings to update

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            user = self.session.query(User).filter_by(id=user_id).first()

            if not user:
                raise UserNotFoundError("User not found")

            # Update allowed settings
            allowed_settings = [
                "theme_preference",
                "language",
                "notification_enabled",
                "budget_alert_enabled",
                "budget_alert_percentage",
            ]

            for key, value in settings.items():
                if key in allowed_settings:
                    setattr(user, key, value)

            user.updated_at = datetime.utcnow()
            self.session.commit()

            logger.info(f"User settings updated: {user_id}")
            return True, "Settings updated successfully"

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating settings: {str(e)}")
            raise AuthenticationException(f"Settings update failed: {str(e)}")

    def deactivate_account(self, user_id: int) -> Tuple[bool, str]:
        """
        Deactivate user account.

        Args:
            user_id: User ID

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            user = self.session.query(User).filter_by(id=user_id).first()

            if not user:
                raise UserNotFoundError("User not found")

            user.is_active = False
            user.updated_at = datetime.utcnow()
            self.session.commit()

            logger.info(f"User account deactivated: {user_id}")
            return True, "Account deactivated successfully"

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deactivating account: {str(e)}")
            raise AuthenticationException(f"Account deactivation failed: {str(e)}")
