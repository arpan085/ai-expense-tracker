"""
Database Module

Handles database initialization, connection management, and session management.
"""

from typing import Generator, Optional
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import Engine
from app.config import settings
from app.logger import get_logger
from app.models import init_db, Base
from app.exceptions import DatabaseConnectionError, DatabaseQueryError

logger = get_logger(__name__)


class Database:
    """Database connection and session management."""

    _instance: Optional["Database"] = None
    _engine: Optional[Engine] = None
    _SessionLocal: Optional[sessionmaker] = None

    def __new__(cls) -> "Database":
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize database connection."""
        if self._engine is None:
            self._initialize()

    def _initialize(self) -> None:
        """Initialize database engine and session factory."""
        try:
            logger.info(f"Initializing database: {settings.DATABASE_URL}")

            self._engine, self._SessionLocal = init_db(settings.DATABASE_URL)

            logger.info("Database initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise DatabaseConnectionError(f"Failed to connect to database: {str(e)}")

    @property
    def engine(self) -> Engine:
        """Get database engine."""
        if self._engine is None:
            self._initialize()
        return self._engine

    @property
    def SessionLocal(self) -> sessionmaker:
        """Get session factory."""
        if self._SessionLocal is None:
            self._initialize()
        return self._SessionLocal

    def get_session(self) -> Session:
        """
        Get a new database session.

        Returns:
            SQLAlchemy session
        """
        if self._SessionLocal is None:
            self._initialize()
        return self._SessionLocal()

    def get_session_generator(self) -> Generator[Session, None, None]:
        """
        Get a session generator for dependency injection.

        Yields:
            SQLAlchemy session
        """
        session = self.get_session()
        try:
            yield session
        finally:
            session.close()

    def close(self) -> None:
        """Close database connection."""
        if self._engine:
            self._engine.dispose()
            logger.info("Database connection closed")

    def create_tables(self) -> None:
        """Create all database tables."""
        try:
            Base.metadata.create_all(bind=self._engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {str(e)}")
            raise DatabaseQueryError(f"Failed to create tables: {str(e)}")

    def drop_tables(self) -> None:
        """
        Drop all database tables.

        WARNING: This will delete all data!
        """
        try:
            Base.metadata.drop_all(bind=self._engine)
            logger.warning("All database tables dropped")
        except Exception as e:
            logger.error(f"Failed to drop tables: {str(e)}")
            raise DatabaseQueryError(f"Failed to drop tables: {str(e)}")

    def seed_sample_data(self) -> None:
        """Seed database with sample data for testing."""
        from datetime import datetime, timedelta
        from app.models import User, Expense, Income, Budget
        from app.security import password_manager

        session = self.get_session()

        try:
            # Check if data already exists
            existing_user = session.query(User).filter_by(username="demo").first()
            if existing_user:
                logger.info("Sample data already exists")
                session.close()
                return

            # Create demo user
            demo_user = User(
                username="demo",
                email="demo@example.com",
                password_hash=password_manager.hash_password("Demo@12345"),
                is_active=True,
                theme_preference="dark",
            )
            session.add(demo_user)
            session.flush()

            # Create sample expenses
            today = datetime.now()
            categories = ["Food", "Transport", "Entertainment", "Utilities", "Shopping"]

            for i in range(20):
                expense = Expense(
                    user_id=demo_user.id,
                    amount=float(10 + (i * 5)),
                    category=categories[i % len(categories)],
                    description=f"Sample expense {i + 1}",
                    date=today - timedelta(days=i),
                )
                session.add(expense)

            # Create sample incomes
            for i in range(5):
                income = Income(
                    user_id=demo_user.id,
                    amount=2000.0 + (i * 500),
                    source="Salary" if i == 0 else "Freelance",
                    description=f"Sample income {i + 1}",
                    date=today - timedelta(days=i * 7),
                )
                session.add(income)

            # Create sample budget
            for category in categories:
                budget = Budget(
                    user_id=demo_user.id,
                    category=category,
                    limit=500.0,
                    spent=0.0,
                    month=today.month,
                    year=today.year,
                )
                session.add(budget)

            session.commit()
            logger.info("Sample data seeded successfully")

        except Exception as e:
            session.rollback()
            logger.error(f"Failed to seed sample data: {str(e)}")
            raise DatabaseQueryError(f"Failed to seed sample data: {str(e)}")

        finally:
            session.close()


# Global database instance
_db_instance: Optional[Database] = None


def get_database() -> Database:
    """
    Get or create database instance (singleton).

    Returns:
        Database instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance


def get_session() -> Session:
    """
    Get a new database session.

    Returns:
        SQLAlchemy session
    """
    return get_database().get_session()


def init_database() -> None:
    """Initialize the database."""
    db = get_database()
    db.create_tables()
    logger.info("Database initialized successfully")


if __name__ == "__main__":
    # Initialize database
    db = get_database()
    db.create_tables()
    db.seed_sample_data()
    logger.info("Database setup complete")
