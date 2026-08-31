"""
Food Rescue Backend — SQLAlchemy Declarative Base.

All models inherit from this base.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass
