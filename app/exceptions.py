"""
Custom Exception Classes

Defines application-specific exceptions for better error handling and reporting.
"""


class AppException(Exception):
    """Base exception for the application."""

    def __init__(self, message: str, code: str = "APP_ERROR"):
        """
        Initialize exception.

        Args:
            message: Error message
            code: Error code for categorization
        """
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self) -> str:
        """String representation of exception."""
        return f"[{self.code}] {self.message}"


class DatabaseException(AppException):
    """Raised when database operations fail."""

    def __init__(self, message: str):
        super().__init__(message, "DATABASE_ERROR")


class DatabaseConnectionError(DatabaseException):
    """Raised when database connection fails."""

    def __init__(self, message: str = "Failed to connect to database"):
        super().__init__(message)


class DatabaseQueryError(DatabaseException):
    """Raised when database query execution fails."""

    def __init__(self, message: str = "Database query execution failed"):
        super().__init__(message)


class AuthenticationException(AppException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTH_ERROR")


class UserNotFoundError(AuthenticationException):
    """Raised when user is not found."""

    def __init__(self, username: str):
        super().__init__(f"User '{username}' not found")


class InvalidCredentialsError(AuthenticationException):
    """Raised when credentials are invalid."""

    def __init__(self, message: str = "Invalid username or password"):
        super().__init__(message)


class UserAlreadyExistsError(AuthenticationException):
    """Raised when trying to register existing user."""

    def __init__(self, username: str):
        super().__init__(f"User '{username}' already exists")


class ValidationException(AppException):
    """Raised when input validation fails."""

    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class InvalidAmountError(ValidationException):
    """Raised when amount is invalid."""

    def __init__(self, amount: str = ""):
        super().__init__(f"Invalid amount: {amount}")


class InvalidDateError(ValidationException):
    """Raised when date is invalid."""

    def __init__(self, date: str = ""):
        super().__init__(f"Invalid date: {date}")


class MissingFieldError(ValidationException):
    """Raised when required field is missing."""

    def __init__(self, field_name: str):
        super().__init__(f"Missing required field: {field_name}")


class BudgetException(AppException):
    """Raised when budget operations fail."""

    def __init__(self, message: str):
        super().__init__(message, "BUDGET_ERROR")


class BudgetExceededError(BudgetException):
    """Raised when budget limit is exceeded."""

    def __init__(self, category: str, limit: float, spent: float):
        message = f"Budget exceeded for {category}. Limit: {limit}, Spent: {spent}"
        super().__init__(message)


class ExportException(AppException):
    """Raised when export operations fail."""

    def __init__(self, message: str):
        super().__init__(message, "EXPORT_ERROR")


class PDFExportError(ExportException):
    """Raised when PDF export fails."""

    def __init__(self, message: str = "PDF export failed"):
        super().__init__(message)


class ExcelExportError(ExportException):
    """Raised when Excel export fails."""

    def __init__(self, message: str = "Excel export failed"):
        super().__init__(message)


class APIException(AppException):
    """Raised when API operations fail."""

    def __init__(self, message: str):
        super().__init__(message, "API_ERROR")


class GoogleAPIError(APIException):
    """Raised when Google API call fails."""

    def __init__(self, message: str = "Google API call failed"):
        super().__init__(message)


class BackupException(AppException):
    """Raised when backup operations fail."""

    def __init__(self, message: str):
        super().__init__(message, "BACKUP_ERROR")


class BackupCreationError(BackupException):
    """Raised when backup creation fails."""

    def __init__(self, message: str = "Failed to create backup"):
        super().__init__(message)


class BackupRestoreError(BackupException):
    """Raised when backup restore fails."""

    def __init__(self, message: str = "Failed to restore backup"):
        super().__init__(message)


class ConfigException(AppException):
    """Raised when configuration is invalid."""

    def __init__(self, message: str):
        super().__init__(message, "CONFIG_ERROR")


class UIException(AppException):
    """Raised when UI operations fail."""

    def __init__(self, message: str):
        super().__init__(message, "UI_ERROR")


class NotificationException(AppException):
    """Raised when notification operations fail."""

    def __init__(self, message: str):
        super().__init__(message, "NOTIFICATION_ERROR")
