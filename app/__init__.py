"""
AI Expense Tracker Application

A professional desktop application for tracking income and expenses 
with AI-powered spending analysis and comprehensive reporting features.
"""

__version__ = "1.0.0"
__author__ = "Arpan"
__description__ = "AI-powered expense tracking application"

from app.config import Settings
from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Load settings
settings = Settings()

__all__ = ["Settings", "logger", "settings"]
