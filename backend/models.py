"""Pydantic models for request/response schemas."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PredictionRequest(BaseModel):
    """Schema for single prediction request."""
    study_hours: float = Field(..., ge=0, le=24, description="Study hours (0-24)")


class PredictionResponse(BaseModel):
    """Schema for single prediction response."""
    study_hours: float
    predicted_marks: float
    confidence: float
    equation: str


class BatchPredictionResult(BaseModel):
    """Schema for a single row in batch prediction."""
    study_hours: float
    predicted_marks: float


class BatchPredictionResponse(BaseModel):
    """Schema for batch prediction response."""
    results: List[BatchPredictionResult]
    total: int
    average_predicted: float


class HistoryEntry(BaseModel):
    """Schema for prediction history entry."""
    id: int
    study_hours: float
    predicted_marks: float
    timestamp: str
    prediction_type: str  # "single" or "batch"


class MetricsResponse(BaseModel):
    """Schema for model metrics response."""
    mae: float
    mse: float
    rmse: float
    r2_score: float
    confidence: float
    equation: str
    training_samples: int
    testing_samples: int


class ChartDataResponse(BaseModel):
    """Schema for chart data response."""
    scatter: dict
    regression: dict
    histogram: dict


class RetrainResponse(BaseModel):
    """Schema for retrain response."""
    message: str
    old_metrics: Optional[MetricsResponse] = None
    new_metrics: MetricsResponse


class DatasetInfoResponse(BaseModel):
    """Schema for dataset info response."""
    rows: int
    columns: List[str]
    shape: List[int]
    null_values: dict
    statistics: dict
    sample_data: List[dict]
