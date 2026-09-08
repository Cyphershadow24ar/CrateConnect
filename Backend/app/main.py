"""
Food Rescue Backend — FastAPI Application Entry Point.
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    health,
    category,
    business,
    inventory,
    transaction,
    pos,
)
from app.core.config import settings
from app.core.errors import (
    AppError,
    app_error_handler,
    generic_error_handler,
    validation_error_handler,
)


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title="Food Rescue API",
        description="AI-Powered Food Waste Management Platform — Milestone 1",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # ── CORS ──────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Error Handlers ────────────────────────────────────
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, generic_error_handler)

    # ── Routes ────────────────────────────────────────────
    app.include_router(health.router, prefix="/api/v1")
    app.include_router(category.router, prefix="/api/v1")
    app.include_router(business.router, prefix="/api/v1")
    app.include_router(inventory.router, prefix="/api/v1")
    app.include_router(transaction.router, prefix="/api/v1")
    app.include_router(pos.router, prefix="/api/v1")
    return app


app = create_app()
