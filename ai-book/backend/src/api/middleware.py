"""
Request middleware for logging, error handling, and correlation IDs.
"""

import logging
import time
import uuid
from contextvars import ContextVar
from typing import Callable

from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

# Context variable for correlation ID
correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id", default="")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests with correlation IDs."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log details."""
        # Generate or extract correlation ID
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        correlation_id_ctx.set(correlation_id)

        # Start timing
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000

        # Log request details
        logger.info(
            f"[{correlation_id}] {request.method} {request.url.path} "
            f"status={response.status_code} duration={duration_ms:.2f}ms"
        )

        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id

        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for consistent error handling."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with error handling."""
        try:
            return await call_next(request)
        except RequestValidationError as exc:
            # Handle validation errors with detailed messages
            errors = exc.errors()
            error_messages = [
                f"{'.'.join(str(loc) for loc in error['loc'])}: {error['msg']}"
                for error in errors
            ]

            logger.warning(
                f"[{correlation_id_ctx.get()}] Validation error: {error_messages}"
            )

            return JSONResponse(
                status_code=422,
                content={
                    "error": "Validation Error",
                    "message": "Request validation failed",
                    "details": error_messages,
                    "correlation_id": correlation_id_ctx.get(),
                },
            )
        except ValueError as exc:
            # Handle value errors (e.g., invalid parameters)
            logger.warning(
                f"[{correlation_id_ctx.get()}] Value error: {str(exc)}"
            )

            return JSONResponse(
                status_code=400,
                content={
                    "error": "Bad Request",
                    "message": str(exc),
                    "correlation_id": correlation_id_ctx.get(),
                },
            )
        except Exception as exc:
            # Handle unexpected errors
            logger.exception(
                f"[{correlation_id_ctx.get()}] Unexpected error: {str(exc)}"
            )

            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                    "correlation_id": correlation_id_ctx.get(),
                },
            )


def get_correlation_id() -> str:
    """Get the current correlation ID from context."""
    return correlation_id_ctx.get()


def setup_middleware(app):
    """Add middleware to FastAPI app."""
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)
