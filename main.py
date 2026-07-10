"""
Main Application Entry Point

This is the entry point for the AI Expense Tracker desktop application.
Run this file to start the application.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.config import settings
from app.logger import setup_logger
from app.database import get_database, init_database
from app.exceptions import AppException

logger = setup_logger(__name__)


def main():
    """
    Main application entry point.
    
    Initializes database, sets up configuration, and starts the UI.
    """
    try:
        logger.info("=" * 60)
        logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        logger.info("=" * 60)

        # Initialize database
        logger.info("Initializing database...")
        init_database()
        logger.info("Database initialized successfully")

        # Import UI after database initialization
        from app.ui.main_window import MainWindow
        import customtkinter as ctk

        logger.info("Initializing UI...")

        # Configure theme
        ctk.set_appearance_mode(settings.THEME)
        ctk.set_default_color_theme("blue")

        # Create and run main window
        root = ctk.CTk()
        root.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        root.title(f"{settings.APP_NAME} v{settings.APP_VERSION}")

        # Center window on screen
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - settings.WINDOW_WIDTH) // 2
        y = (screen_height - settings.WINDOW_HEIGHT) // 2
        root.geometry(f"+{x}+{y}")

        # Create main window
        app = MainWindow(root)

        logger.info("Application UI initialized successfully")
        logger.info(f"Window size: {settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        logger.info(f"Theme: {settings.THEME}")

        logger.info("Starting main event loop...")
        root.mainloop()

        logger.info("Application closed")

    except ImportError as e:
        logger.error(f"Import Error: {str(e)}")
        logger.error("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)

    except AppException as e:
        logger.error(f"Application Error: {str(e)}")
        sys.exit(1)

    except Exception as e:
        logger.critical(f"Unexpected Error: {str(e)}", exc_info=True)
        sys.exit(1)

    finally:
        logger.info("=" * 60)
        logger.info(f"Shutting down {settings.APP_NAME}")
        logger.info("=" * 60)

        # Cleanup
        try:
            db = get_database()
            db.close()
            logger.info("Database connection closed")
        except Exception as e:
            logger.warning(f"Error closing database: {str(e)}")


if __name__ == "__main__":
    main()
