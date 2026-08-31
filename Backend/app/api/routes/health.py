"""Health check endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(tags=["health"])

_db_dep = Depends(get_db)


@router.get("/health")
def health_check(db: Session = _db_dep):
    """
    Service and database health summary.

    Returns service status and database connectivity.
    """
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "ok" if db_status == "healthy" else "degraded",
        "service": "food-rescue-api",
        "database": db_status,
    }
