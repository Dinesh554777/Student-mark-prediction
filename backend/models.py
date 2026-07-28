"""Pydantic models for request/response schemas."""

from pydantic import BaseModel, Field
from typing import List, Optional


class PredictionRequest(BaseModel):
    """Schema for single prediction request."""
    study_hours: float = Field(..., ge=0, le=24, description="Study hours (0-24)")
    attendance: float = Field(0, ge=0, le=100, description="Attendance percentage (0-100)")
    sleep_hours: float = Field(0, ge=0, le=24, description="Sleep hours (0-24)")
    previous_score: float = Field(0, ge=0, le=100, description="Previous score (0-100)")


class PredictionResponse(BaseModel):
    """Schema for single prediction response."""
    study_hours: float
    predicted_marks: float
    confidence: float
    equation: str
    features_used: List[str]


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
    attendance: float = 0
    sleep_hours: float = 0
    previous_score: float = 0
    predicted_marks: float
    timestamp: str
    prediction_type: str


class HistoryStats(BaseModel):
    """Schema for history statistics."""
    total: int
    avg_marks: float = 0
    min_marks: float = 0
    max_marks: float = 0
    avg_hours: float = 0


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


class RechartsScatterPoint(BaseModel):
    x: float
    y: float


class RechartsLinePoint(BaseModel):
    x: float
    y: float


class RechartsBarItem(BaseModel):
    name: str
    value: int


class RechartsDataResponse(BaseModel):
    """Schema for Recharts-compatible chart data."""
    scatter: List[RechartsScatterPoint]
    regression_line: List[RechartsLinePoint]
    study_hours_dist: List[RechartsBarItem]
    marks_dist: List[RechartsBarItem]


class ChartDataResponse(BaseModel):
    """Schema for matplotlib chart data (base64)."""
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
