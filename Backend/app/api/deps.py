"""
API Dependencies — shared FastAPI dependencies.

Provides database session and tenant context injection.
"""

import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db


def get_current_business_id() -> uuid.UUID:
    """
    Return the current business/tenant ID.

    Milestone 1: returns the deterministic demo business ID.
    Future: will resolve from authentication token.
    """
    return uuid.UUID(settings.DEMO_BUSINESS_ID)


def get_db_session() -> Session:  # type: ignore[misc]
    """Alias for get_db — used as a FastAPI dependency."""
    yield from get_db()


# Type aliases for cleaner route signatures
DBSession = Depends(get_db_session)
CurrentBusinessId = Depends(get_current_business_id)
