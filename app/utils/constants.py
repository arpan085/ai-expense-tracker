"""
Utility Constants

Application-wide constants for categories, colors, and configuration.
"""

from typing import Dict, List

# Expense Categories
EXPENSE_CATEGORIES: List[str] = [
    "Food & Dining",
    "Transportation",
    "Entertainment",
    "Utilities",
    "Shopping",
    "Healthcare",
    "Education",
    "Travel",
    "Personal Care",
    "Home",
    "Insurance",
    "Other",
]

# Income Sources
INCOME_SOURCES: List[str] = [
    "Salary",
    "Freelance",
    "Investment",
    "Bonus",
    "Gift",
    "Refund",
    "Other",
]

# Color Palette for Dark Mode
DARK_MODE_COLORS: Dict[str, str] = {
    "bg_primary": "#1a1a2e",
    "bg_secondary": "#16213e",
    "bg_tertiary": "#0f3460",
    "text_primary": "#eaeaea",
    "text_secondary": "#b0b0b0",
    "accent": "#e94560",
    "success": "#00d4ff",
    "warning": "#ffa500",
    "error": "#ff6b6b",
    "border": "#2c2c54",
}

# Color Palette for Light Mode
LIGHT_MODE_COLORS: Dict[str, str] = {
    "bg_primary": "#ffffff",
    "bg_secondary": "#f5f5f5",
    "bg_tertiary": "#e8e8e8",
    "text_primary": "#1a1a1a",
    "text_secondary": "#555555",
    "accent": "#e94560",
    "success": "#00b366",
    "warning": "#ffa500",
    "error": "#ff6b6b",
    "border": "#cccccc",
}

# Notification Types
NOTIFICATION_TYPE_INFO = "info"
NOTIFICATION_TYPE_SUCCESS = "success"
NOTIFICATION_TYPE_WARNING = "warning"
NOTIFICATION_TYPE_ERROR = "error"

NOTIFICATION_TYPES: List[str] = [
    NOTIFICATION_TYPE_INFO,
    NOTIFICATION_TYPE_SUCCESS,
    NOTIFICATION_TYPE_WARNING,
    NOTIFICATION_TYPE_ERROR,
]

# Date Formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DISPLAY_DATE_FORMAT = "%d %b %Y"
DISPLAY_DATETIME_FORMAT = "%d %b %Y, %H:%M"

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Backup
BACKUP_EXTENSION = ".backup"
MAX_BACKUP_FILES = 10

# File Extensions
PDF_EXTENSION = ".pdf"
EXCEL_EXTENSION = ".xlsx"
CSV_EXTENSION = ".csv"

# API
GOOGLE_API_TIMEOUT = 30

# UI
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700

# Session
SESSION_TIMEOUT_SECONDS = 3600  # 1 hour

# Rate Limiting
MAX_LOGIN_ATTEMPTS = 5
LOGIN_RATE_LIMIT_WINDOW = 300  # 5 minutes

# Export Limits
MAX_EXPORT_RECORDS = 10000
EXPORT_BATCH_SIZE = 1000

# Budget
DEFAULT_BUDGET_ALERT_PERCENTAGE = 80.0

# Currency
DEFAULT_CURRENCY = "USD"
CURRENCY_SYMBOLS: Dict[str, str] = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "INR": "₹",
}

# Message Templates
MESSAGE_LOGIN_SUCCESS = "Login successful! Welcome {username}."
MESSAGE_LOGIN_FAILED = "Login failed. Please check your credentials."
MESSAGE_REGISTRATION_SUCCESS = "Account created successfully! Please login."
MESSAGE_REGISTRATION_FAILED = "Registration failed. Please try again."
MESSAGE_EXPENSE_ADDED = "Expense added successfully."
MESSAGE_EXPENSE_UPDATED = "Expense updated successfully."
MESSAGE_EXPENSE_DELETED = "Expense deleted successfully."
MESSAGE_INCOME_ADDED = "Income added successfully."
MESSAGE_INCOME_UPDATED = "Income updated successfully."
MESSAGE_INCOME_DELETED = "Income deleted successfully."
MESSAGE_BUDGET_EXCEEDED = "Budget limit exceeded for {category}!"
MESSAGE_BUDGET_NEAR_LIMIT = "You're nearing your budget limit for {category}."
MESSAGE_EXPORT_SUCCESS = "Data exported successfully."
MESSAGE_EXPORT_FAILED = "Export failed. Please try again."
MESSAGE_BACKUP_SUCCESS = "Backup created successfully."
MESSAGE_BACKUP_FAILED = "Backup creation failed."

# Placeholder Values
PLACEHOLDER_USERNAME = "Enter username"
PLACEHOLDER_EMAIL = "Enter email address"
PLACEHOLDER_PASSWORD = "Enter password"
PLACEHOLDER_AMOUNT = "0.00"
PLACEHOLDER_DESCRIPTION = "Optional description"
PLACEHOLDER_SEARCH = "Search records..."
