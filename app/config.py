"""
Application Configuration Management

This module handles all configuration settings for the application,
including database, API keys, UI settings, and security parameters.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings using Pydantic BaseSettings.
    
    Loads configuration from environment variables and .env file.
    """

    # Application
    APP_NAME: str = "AI Expense Tracker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, alias="DEBUG")

    # Database
    DATABASE_PATH: str = Field(default="data/expenses.db", alias="DATABASE_PATH")
    DATABASE_BACKUP_PATH: str = Field(default="backup/", alias="DATABASE_BACKUP_PATH")
    DATABASE_URL: Optional[str] = None

    # API Keys
    GOOGLE_API_KEY: Optional[str] = Field(default=None, alias="GOOGLE_API_KEY")

    # UI Configuration
    THEME: str = Field(default="dark", alias="THEME")
    LANGUAGE: str = Field(default="en", alias="LANGUAGE")
    WINDOW_WIDTH: int = Field(default=1400, alias="WINDOW_WIDTH")
    WINDOW_HEIGHT: int = Field(default=900, alias="WINDOW_HEIGHT")
    ENABLE_DARK_MODE: bool = Field(default=True, alias="ENABLE_DARK_MODE")
    ENABLE_ANIMATIONS: bool = Field(default=True, alias="ENABLE_ANIMATIONS")
    ENABLE_CHARTS: bool = Field(default=True, alias="ENABLE_CHARTS")
    ENABLE_AI_ANALYSIS: bool = Field(default=True, alias="ENABLE_AI_ANALYSIS")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", alias="LOG_LEVEL")
    LOG_FILE: str = Field(default="logs/app.log", alias="LOG_FILE")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        alias="LOG_FORMAT"
    )

    # Security
    PASSWORD_MIN_LENGTH: int = Field(default=8, alias="PASSWORD_MIN_LENGTH")
    SESSION_TIMEOUT: int = Field(default=3600, alias="SESSION_TIMEOUT")
    MAX_LOGIN_ATTEMPTS: int = Field(default=5, alias="MAX_LOGIN_ATTEMPTS")
    BCRYPT_ROUNDS: int = Field(default=12, alias="BCRYPT_ROUNDS")

    # Notifications
    ENABLE_NOTIFICATIONS: bool = Field(default=True, alias="ENABLE_NOTIFICATIONS")
    BUDGET_ALERT_PERCENTAGE: float = Field(default=80.0, alias="BUDGET_ALERT_PERCENTAGE")

    # Backup
    BACKUP_ENABLED: bool = Field(default=True, alias="BACKUP_ENABLED")
    BACKUP_INTERVAL: int = Field(default=86400, alias="BACKUP_INTERVAL")
    AUTO_BACKUP_ON_EXIT: bool = Field(default=True, alias="AUTO_BACKUP_ON_EXIT")
    MAX_BACKUPS: int = Field(default=10, alias="MAX_BACKUPS")

    # Features
    ENABLE_PDF_EXPORT: bool = Field(default=True, alias="ENABLE_PDF_EXPORT")
    ENABLE_EXCEL_EXPORT: bool = Field(default=True, alias="ENABLE_EXCEL_EXPORT")

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def __init__(self, **data):
        """Initialize settings and create necessary directories."""
        super().__init__(**data)
        self._setup_database_url()
        self._create_directories()

    def _setup_database_url(self) -> None:
        """Setup database URL for SQLAlchemy."""
        if not self.DATABASE_URL:
            db_path = Path(self.DATABASE_PATH)
            self.DATABASE_URL = f"sqlite:///{db_path.absolute()}"

    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            Path(self.DATABASE_PATH).parent,
            Path(self.LOG_FILE).parent,
            Path(self.DATABASE_BACKUP_PATH),
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.DEBUG

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.DEBUG

    @property
    def database_file_path(self) -> Path:
        """Get database file path as Path object."""
        return Path(self.DATABASE_PATH)

    @property
    def log_file_path(self) -> Path:
        """Get log file path as Path object."""
        return Path(self.LOG_FILE)

    @property
    def backup_directory_path(self) -> Path:
        """Get backup directory path as Path object."""
        return Path(self.DATABASE_BACKUP_PATH)


# Global settings instance
settings = Settings()
