"""
Database Models using SQLAlchemy ORM

Defines all database models for the application with relationships and constraints.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, String, Float, DateTime, Integer, Boolean, ForeignKey,
    Index, Text, create_engine, event
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """User model for authentication and profile management."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, nullable=False)
    theme_preference = Column(String(10), default="dark", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    last_login = Column(DateTime, nullable=True)
    notification_enabled = Column(Boolean, default=True, nullable=False)
    budget_alert_enabled = Column(Boolean, default=True, nullable=False)
    budget_alert_percentage = Column(Float, default=80.0, nullable=False)

    # Relationships
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    incomes = relationship("Income", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"


class Expense(Base):
    """Expense model for tracking expenditures."""

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False, index=True)
    tags = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    notes = Column(Text, nullable=True)
    receipt_path = Column(String(255), nullable=True)

    # Relationships
    user = relationship("User", back_populates="expenses")

    # Indexes
    __table_args__ = (
        Index("idx_user_date", "user_id", "date"),
        Index("idx_category_date", "category", "date"),
    )

    def __repr__(self) -> str:
        return f"<Expense(id={self.id}, amount={self.amount}, category='{self.category}')>"


class Income(Base):
    """Income model for tracking earnings."""

    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    source = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False, index=True)
    tags = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="incomes")

    # Indexes
    __table_args__ = (
        Index("idx_user_income_date", "user_id", "date"),
        Index("idx_source_date", "source", "date"),
    )

    def __repr__(self) -> str:
        return f"<Income(id={self.id}, amount={self.amount}, source='{self.source}')>"


class Budget(Base):
    """Budget model for tracking budget limits per category."""

    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String(50), nullable=False)
    limit = Column(Float, nullable=False)
    spent = Column(Float, default=0.0, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    alert_sent = Column(Boolean, default=False, nullable=False)

    # Relationships
    user = relationship("User", back_populates="budgets")

    # Indexes
    __table_args__ = (
        Index("idx_user_category_month", "user_id", "category", "month", "year"),
    )

    def __repr__(self) -> str:
        return f"<Budget(id={self.id}, category='{self.category}', limit={self.limit})>"

    @property
    def percentage_spent(self) -> float:
        """Calculate percentage of budget spent."""
        if self.limit == 0:
            return 0
        return (self.spent / self.limit) * 100

    @property
    def remaining(self) -> float:
        """Calculate remaining budget."""
        return max(0, self.limit - self.spent)


class Notification(Base):
    """Notification model for user alerts and notifications."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(
        String(50),
        nullable=False,
        default="info"
    )
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    read_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="notifications")

    # Indexes
    __table_args__ = (
        Index("idx_user_read", "user_id", "is_read"),
    )

    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, title='{self.title}')>"


class AuditLog(Base):
    """Audit log model for tracking user actions."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=True)
    old_values = Column(Text, nullable=True)
    new_values = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False, index=True)

    # Indexes
    __table_args__ = (
        Index("idx_user_action", "user_id", "action"),
        Index("idx_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action='{self.action}', entity='{self.entity_type}')>"


# Database initialization
def init_db(database_url: str) -> tuple:
    """
    Initialize database connection and create all tables.

    Args:
        database_url: SQLAlchemy database URL

    Returns:
        Tuple of (engine, SessionLocal)
    """
    engine = create_engine(
        database_url,
        echo=False,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
    )

    # Enable foreign keys for SQLite
    if "sqlite" in database_url:
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return engine, SessionLocal
