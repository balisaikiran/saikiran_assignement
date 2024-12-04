"""API documentation configuration."""
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

def custom_openapi(app: FastAPI):
    """Configure custom OpenAPI documentation."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="NYC Taxi Trip Data Service",
        version="1.0.0",
        description="""
        API service for New York City taxi trip data analysis.
        
        Features:
        - Query trip data with various filters
        - Get statistical analysis of trips
        - Upload and process new trip data
        - Advanced analytics and visualizations
        """,
        routes=app.routes,
    )
    
    # Add security scheme if needed
    # openapi_schema["components"]["securitySchemes"] = {...}
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema