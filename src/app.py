"""FastAPI web application for LexLang."""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import logging
from datetime import datetime

from .config import load_config
from .core.pipeline import Pipeline
from .api.models import (
    ProcessRequest, ProcessResponse, 
    AnalysisRequest, AnalysisResponse,
    TrainingRequest, TrainingResponse
)
from .api.middleware import setup_middleware
from .api.auth import get_current_user
from .exceptions import LexLangError
from .utils import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LexLang API",
    description="Advanced NLP API for Ewe language processing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup middleware
setup_middleware(app)

# Global variables
config = None
pipeline = None


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    global config, pipeline
    try:
        config = load_config("configs/default.yaml")
        pipeline = Pipeline(config)
        logger.info("LexLang API started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "LexLang API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@app.post("/process", response_model=ProcessResponse)
async def process_text(
    request: ProcessRequest,
    background_tasks: BackgroundTasks,
    current_user: Optional[str] = Depends(get_current_user)
):
    """Process text with specified tasks."""
    try:
        results = pipeline.process(
            text=request.text,
            dialect=request.dialect,
            tasks=request.tasks,
            output_format=request.output_format
        )
        
        # Log request for analytics
        background_tasks.add_task(
            log_request,
            user_id=current_user,
            request_type="process",
            text_length=len(request.text),
            tasks=request.tasks
        )
        
        return ProcessResponse(
            results=json.loads(results) if request.output_format == "json" else results,
            processing_time=0.0,  # TODO: Implement timing
            dialect_detected=request.dialect,
            tasks_completed=request.tasks
        )
        
    except LexLangError as e:
        logger.error(f"Processing error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(
    request: AnalysisRequest,
    current_user: Optional[str] = Depends(get_current_user)
):
    """Perform comprehensive text analysis."""
    try:
        # Run full analysis pipeline
        results = pipeline.process(
            text=request.text,
            dialect="auto",
            tasks=["tokenize", "normalize", "pos", "tone", "dialect"],
            output_format="json"
        )
        
        parsed_results = json.loads(results)
        
        return AnalysisResponse(
            tokens=parsed_results.get("tokens", []),
            pos_tags=parsed_results.get("pos_tags", []),
            tonal_analysis=parsed_results.get("tonal_analysis", {}),
            dialect_info=parsed_results.get("dialect_info", {}),
            morphological_analysis=parsed_results.get("morphological_analysis", {}),
            linguistic_features=parsed_results.get("linguistic_features", {})
        )
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")


@app.get("/models")
async def list_models():
    """List available models."""
    try:
        models = {
            "pos_tagger": "v1.2",
            "dialect_classifier": "v3.0",
            "tone_classifier": "v2.5",
            "embeddings": "v2.1",
            "transformers": "v1.0"
        }
        return {"models": models}
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail="Failed to list models")


@app.get("/dialects")
async def list_dialects():
    """List supported dialects."""
    return {
        "dialects": [
            {"code": "anlo", "name": "Anlo", "region": "South-East Ghana"},
            {"code": "inland", "name": "Inland", "region": "Central Ghana"},
            {"code": "ho", "name": "Ho", "region": "Volta Region"},
            {"code": "kpando", "name": "Kpando", "region": "Volta Region"}
        ]
    }


async def log_request(user_id: Optional[str], request_type: str, 
                     text_length: int, tasks: List[str]):
    """Log request for analytics."""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "request_type": request_type,
        "text_length": text_length,
        "tasks": tasks
    }
    logger.info(f"Request logged: {json.dumps(log_data)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
