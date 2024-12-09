"""Main application entry point."""
from src.database.models import Base
import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.graphql import GraphQLApp
from src.api.rest import router as rest_router
from src.database.connection import DatabaseManager
from src.api.graphql import schema
from src.config.settings import Settings
from src.cache.redis_manager import RedisManager
from src.middleware.error_handler import error_handler
from src.middleware.rate_limiter import RateLimiter
from src.auth.jwt_handler import JWTHandler
from fastapi.openapi.docs import get_swagger_ui_html
from src.api.docs import custom_openapi

# Initialize settings and services
settings = Settings()
db_manager = DatabaseManager(settings.DATABASE_URL)
redis_manager = RedisManager(settings)
rate_limiter = RateLimiter(redis_manager, settings.RATE_LIMIT_PER_MINUTE)

# Create database tables
Base.metadata.create_all(bind=db_manager.engine)

# Initialize FastAPI application
app = FastAPI(
    title="NYC Taxi Trip Data Service",
    description="API service for analyzing NYC taxi trip data",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

# Custom API documentation
app.openapi = lambda: custom_openapi(app)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="NYC Taxi Trip Data Service - API Documentation",
        swagger_favicon_url="/static/favicon.ico"
    )

# Add middleware
app.middleware("http")(error_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting dependency
async def check_rate_limit(request: Request):
    await rate_limiter.check_rate_limit(request)

# Include routers
app.include_router(rest_router, prefix="/api/v1")

# Remove the direct route addition with dependencies
# Instead, create a dependency-protected endpoint that serves GraphQL

@app.post("/graphql")
@app.get("/graphql")
async def graphql_endpoint(request: Request):
    await check_rate_limit(request)
    return await GraphQLApp(schema=schema)(request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)