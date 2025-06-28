"""
Pydantic models for API requests and responses.
These models define the data structures for communication with the LexLang API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ProcessRequest(BaseModel):
    """Request model for text processing."""
    text: str = Field(..., example="Ɖeka, eve, etɔ̃.", description="Input text to be processed.")
    dialect: Optional[str] = Field("auto", example="anlo", description="Target dialect for processing (e.g., 'anlo', 'inland', 'ho', 'kpando', or 'auto' for automatic detection).")
    tasks: Optional[List[str]] = Field(["tokenize", "normalize", "pos"], example=["tokenize", "normalize", "tone"], description="List of processing tasks to perform (e.g., 'tokenize', 'normalize', 'pos', 'tone', 'dialect', 'morphology', 'embeddings').")
    output_format: Optional[str] = Field("json", example="json", description="Desired output format ('json', 'text', 'conllu').")

class ProcessResponse(BaseModel):
    """Response model for text processing."""
    results: Any = Field(..., description="Processed results, format depends on output_format in request.")
    processing_time: float = Field(..., example=0.123, description="Time taken for processing in seconds.")
    dialect_detected: Optional[str] = Field(None, example="anlo", description="Detected dialect if 'auto' was specified.")
    tasks_completed: List[str] = Field(..., example=["tokenize", "normalize", "pos"], description="List of tasks successfully completed.")
    
class AnalysisRequest(BaseModel):
    """Request model for comprehensive text analysis."""
    text: str = Field(..., example="Enye gbeŋutiŋutinye.", description="Input text for detailed linguistic analysis.")

class AnalysisResponse(BaseModel):
    """Response model for comprehensive text analysis."""
    tokens: List[str] = Field(..., example=["Enye", "gbeŋutiŋutinye"], description="List of tokens from the text.")
    pos_tags: List[List[str]] = Field(..., example=[["Enye", "PRON"], ["gbeŋutiŋutinye", "NOUN"]], description="List of [token, POS_tag] pairs.")
    tonal_analysis: Dict[str, Any] = Field(..., example={"high_tones": 2, "low_tones": 1}, description="Detailed tonal analysis results.")
    dialect_info: Dict[str, Any] = Field(..., example={"predicted": "anlo", "scores": {"anlo": 0.9, "inland": 0.1}}, description="Information about detected dialect.")
    morphological_analysis: Optional[Dict[str, Any]] = Field(None, description="Detailed morphological analysis results.")
    linguistic_features: Optional[Dict[str, Any]] = Field(None, description="Other extracted linguistic features.")

class TrainingRequest(BaseModel):
    """Request model for model training."""
    model_type: str = Field(..., example="pos", description="Type of model to train (e.g., 'pos', 'dialect', 'tone', 'embeddings').")
    training_data_path: str = Field(..., example="data/corpora/train/mixed_train.txt", description="Path to the training data.")
    output_dir: Optional[str] = Field(None, example="models/custom_models/", description="Directory to save the trained model.")
    params: Optional[Dict[str, Any]] = Field({}, example={"epochs": 10, "learning_rate": 0.001}, description="Optional training parameters.")

class TrainingResponse(BaseModel):
    """Response model for model training."""
    success: bool = Field(..., example=True, description="True if training was successful, False otherwise.")
    model_path: Optional[str] = Field(None, example="models/pos/custom_pos_model.pkl", description="Path to the saved model.")
    metrics: Optional[Dict[str, Any]] = Field(None, example={"loss": 0.05, "accuracy": 0.92}, description="Metrics from the training process.")
    message: Optional[str] = Field(None, example="Model training completed successfully.", description="Detailed message about the training process.")

class ErrorResponse(BaseModel):
    """Standard error response model."""
    detail: str = Field(..., example="Invalid input provided.", description="Error message.")
