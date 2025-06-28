"""
API module for LexLang.
This module initializes the FastAPI application and includes API routes.
"""

from fastapi import FastAPI
import logging

from .routes import router as api_router, set_pipeline_instance
from .middleware import setup_middleware
from ..config import load_config
from ..core.pipeline import Pipeline
from ..utils import setup_logging

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    """
    setup_logging() # Ensure logging is configured early

    app = FastAPI(
        title="LexLang Ewe NLP API",
        description="Comprehensive NLP API for the Ewe language, supporting dialectal variations and tonal analysis.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Load configuration
    try:
        config = load_config("configs/default.yaml")
        logger.info("Configuration loaded for API.")
    except Exception as e:
        logger.error(f"Failed to load configuration for API: {e}")
        # Depending on severity, you might want to exit or raise an error
        raise RuntimeError(f"API initialization failed: {e}")

    # Initialize the main NLP pipeline
    try:
        pipeline = Pipeline(config)
        set_pipeline_instance(pipeline) # Pass the initialized pipeline to the routes
        logger.info("NLP Pipeline initialized for API.")
    except Exception as e:
        logger.error(f"Failed to initialize NLP pipeline: {e}")
        raise RuntimeError(f"API initialization failed: {e}")

    # Setup middlewares
    setup_middleware(app, config)

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    logger.info("API routes included under /api/v1.")

    @app.get("/")
    async def root():
        return {"message": "Welcome to LexLang Ewe NLP API! Visit /docs for API documentation."}

    return app

# If this file is run directly (e.g., for local testing with `uvicorn src.api.__init__:app`),
# create the app instance.
app = create_app()

# This is the entry point for uvicorn: uvicorn src.api.__init__:app --reload
