"""
API routes for LexLang.
This module defines the FastAPI endpoints for processing, analysis, and model management.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from typing import List, Optional, Dict, Any
import json
import logging

from ..core.pipeline import Pipeline # Assuming Pipeline is accessible
from ..exceptions import LexLangError
from .models import (
    ProcessRequest, ProcessResponse, 
    AnalysisRequest, AnalysisResponse,
    TrainingRequest, TrainingResponse,
    ErrorResponse
)
from .auth import get_current_user # Assuming a simple auth mechanism

router = APIRouter()
logger = logging.getLogger(__name__)

# This should ideally be initialized once by the main app or a dependency injection system
# For simplicity, we assume 'pipeline_instance' is globally available or passed
pipeline_instance: Optional[Pipeline] = None 

def set_pipeline_instance(pipeline: Pipeline):
    """Setter for the pipeline instance."""
    global pipeline_instance
    pipeline_instance = pipeline

@router.get("/health", summary="Health check endpoint", response_description="API status")
async def health_check():
    """
    Provides a simple health check to ensure the API is running.
    """
    return {"status": "healthy", "version": "1.0.0"}

@router.post("/process", response_model=ProcessResponse, summary="Process Ewe text", 
             response_description="Processed text results", responses={400: {"model": ErrorResponse}})
async def process_text(
    request: ProcessRequest,
    background_tasks: BackgroundTasks,
    current_user: Optional[str] = Depends(get_current_user) # Example dependency for auth
):
    """
    Processes the input Ewe text by performing specified NLP tasks such as tokenization,
    normalization, POS tagging, and tonal analysis.
    """
    if pipeline_instance is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Pipeline not initialized.")

    try:
        # Measure processing time
        import time
        start_time = time.perf_counter()
        
        results = pipeline_instance.process(
            text=request.text,
            dialect=request.dialect,
            tasks=request.tasks,
            output_format=request.output_format
        )
        
        end_time = time.perf_counter()
        processing_duration = end_time - start_time

        # Log request for analytics (non-blocking)
        background_tasks.add_task(
            log_request_analytics,
            user_id=current_user,
            request_type="process",
            text_length=len(request.text),
            tasks=request.tasks
        )
        
        return ProcessResponse(
            results=json.loads(results) if request.output_format == "json" else results,
            processing_time=processing_duration,
            dialect_detected=request.dialect, # This might be updated by the pipeline
            tasks_completed=request.tasks
        )
        
    except LexLangError as e:
        logger.error(f"Processing error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during processing: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during processing.")


@router.post("/analyze", response_model=AnalysisResponse, summary="Perform detailed linguistic analysis",
             response_description="Detailed linguistic analysis results", responses={500: {"model": ErrorResponse}})
async def analyze_text(request: AnalysisRequest):
    """
    Performs a comprehensive linguistic analysis on the input Ewe text, including
    tokenization, POS tagging, tonal analysis, and dialect information.
    """
    if pipeline_instance is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Pipeline not initialized.")

    try:
        # For analysis, we typically run a full set of tasks
        results_raw = pipeline_instance.process(
            text=request.text,
            dialect="auto", # Always auto-detect for comprehensive analysis
            tasks=["tokenize", "normalize", "pos", "tone", "dialect", "morphology"],
            output_format="json"
        )
        
        parsed_results = json.loads(results_raw)
        
        return AnalysisResponse(
            tokens=parsed_results.get("tokens", []),
            pos_tags=parsed_results.get("pos_tags", []),
            tonal_analysis=parsed_results.get("tonal", {}), # 'tonal' from pipeline
            dialect_info=parsed_results.get("dialect_analysis", {}), # TODO: Ensure this field is set by pipeline
            morphological_analysis=parsed_results.get("morphological", {}), # TODO: Ensure this field is set by pipeline
            linguistic_features=parsed_results.get("linguistic_features", {}) # TODO: Ensure this field is set by pipeline
        )
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to perform comprehensive analysis.")

@router.get("/models", summary="List available models", response_description="List of available models")
async def list_models():
    """
    Retrieves a list of available NLP models and their versions within LexLang.
    """
    # This should ideally read from a MODEL_REGISTRY.json or similar
    # For now, return a static list
    models = {
        "pos_tagger": {"version": "v1.2", "status": "active"},
        "dialect_classifier": {"version": "v3.0", "status": "active"},
        "tone_classifier": {"version": "v2.5", "status": "active"},
        "embeddings": {"version": "v2.1", "status": "active"},
        "transformer_base": {"version": "v1.0", "status": "active"}
    }
    return {"available_models": models}

@router.get("/dialects", summary="List supported Ewe dialects", response_description="List of supported dialects")
async def list_dialects():
    """
    Returns a list of Ewe dialects supported by the LexLang system.
    """
    supported_dialects = [
        {"code": "anlo", "name": "Anlo Ewe", "description": "Predominant dialect spoken in southeastern Ghana and parts of Togo."},
        {"code": "inland", "name": "Inland Ewe", "description": "Dialects spoken in inland regions, often with distinct tonal patterns."},
        {"code": "ho", "name": "Ho Ewe", "description": "Specific dialect centered around Ho in Ghana's Volta Region."},
        {"code": "kpando", "name": "Kpando Ewe", "description": "Specific dialect spoken around Kpando, Ghana."},
        {"code": "auto", "name": "Automatic Detection", "description": "System will attempt to detect the dialect automatically."}
    ]
    return {"supported_dialects": supported_dialects}


# Background task for analytics
async def log_request_analytics(user_id: Optional[str], request_type: str, text_length: int, tasks: List[str]):
    """Logs request details for analytics purposes."""
    log_data = {
        "timestamp": json.dumps({"$date": {"$numberLong": str(int(time.time() * 1000))}}), # ISO format for better consistency
        "user_id": user_id,
        "request_type": request_type,
        "text_length": text_length,
        "tasks": tasks
    }
    logger.info(f"API Request Log: {json.dumps(log_data)}")
