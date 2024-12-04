"""Global error handling middleware."""
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from ..utils.logging import get_logger

logger = get_logger(__name__)

async def error_handler(request: Request, call_next):
    """Global error handling middleware."""
    try:
        return await call_next(request)
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Database error occurred"}
        )
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )