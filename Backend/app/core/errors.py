"""
Food Rescue Backend — Standardized Error Handling.

Provides a consistent JSON error response shape per BACKEND_STRUCTURE.md §8.
"""

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(HTTPException):
    """Application-level error with structured error response."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: list[dict] | None = None,
    ):
        self.code = code
        self.error_message = message
        self.details = details or []
        super().__init__(status_code=status_code, detail=message)


def error_response(status_code: int, code: str, message: str, details: list[dict] | None = None):
    """Build a standard error JSON response."""
    body = {
        "error": {
            "code": code,
            "message": message,
            "details": details or [],
        }
    }
    return JSONResponse(status_code=status_code, content=body)


async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    """Handle AppError exceptions."""
    return error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.error_message,
        details=exc.details,
    )


async def validation_error_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic / FastAPI request validation errors."""
    details = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err.get("loc", []) if loc != "body")
        details.append({
            "field": field or "unknown",
            "message": err.get("msg", "Validation error."),
        })
    return error_response(
        status_code=422,
        code="VALIDATION_ERROR",
        message="Request validation failed.",
        details=details,
    )


async def generic_error_handler(_request: Request, _exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions without leaking stack traces."""
    return error_response(
        status_code=500,
        code="INTERNAL_ERROR",
        message="An unexpected error occurred.",
    )
