"""
FastAPI middleware configuration for LexLang API.
This module sets up cross-origin resource sharing (CORS) and potentially other middlewares.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger(__name__)

def setup_middleware(app: FastAPI, config: Any = None): # 'Any' for config until LexLangConfig is available
    """
    Configures and adds essential middleware to the FastAPI application.
    
    Args:
        app: The FastAPI application instance.
        config: The LexLang configuration object, if available.
    """
    
    # Configure CORS (Cross-Origin Resource Sharing)
    # Allows frontend applications from different origins to make requests.
    cors_origins = ["*"] # Default to allow all origins for development
    if config and hasattr(config, 'api') and hasattr(config.api, 'cors_origins'):
        cors_origins = config.api.cors_origins
        logger.info(f"CORS origins configured: {cors_origins}")
    else:
        logger.warning("CORS origins not specified in config, allowing all origins (*).")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,          # Allows specified origins (e.g., ["http://localhost:3000"])
        allow_credentials=True,             # Allows cookies to be included in cross-origin requests
        allow_methods=["*"],                # Allows all standard HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],                # Allows all headers in the request
    )
    logger.info("CORS middleware added.")

    # You can add other middlewares here, for example:
    # - Rate limiting (e.g., using `fastapi-limiter`)
    # - Logging middleware
    # - Custom authentication/authorization middleware (beyond simple API key check)

    # Example of a simple custom logging middleware (can be expanded)
    @app.middleware("http")
    async def log_requests(request, call_next):
        logger.debug(f"Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        logger.debug(f"Outgoing response: {response.status_code}")
        return response
    logger.info("Request logging middleware added.")
