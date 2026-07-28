"""ML engine for model loading, training, and prediction."""

import os
import sys
import numpy as np
import joblib
import base64
from io import BytesIO
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "marks_model.pkl")
DATASET_PATH = os.path.join(PROJECT_ROOT, "dataset", "student_marks.csv")

_model = None
_metrics = None


def get_model():
    """Load or return cached model."""
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Train first.")
        _model = joblib.load(MODEL_PATH)
    return _model


def invalidate_model_cache():
    """Force model reload on next access."""
    global _model, _metrics
    _model = None
    _metrics = None


def load_dataset():
    """Load the student marks dataset."""
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")
    return pd.read_csv(DATASET_PATH)


def predict(study_hours: float) -> dict:
    """Predict marks for a single study hours value."""
    model = get_model()
    prediction = model.predict([[study_hours]])[0]
    slope = model.coef_[0]
    intercept = model.intercept_
    return {
        "study_hours": study_hours,
        "predicted_marks": round(prediction, 2),
        "equation": f"Marks = {slope:.2f} * Study_Hours + {intercept:.2f}",
    }


def predict_batch(study_hours_list: list) -> list:
    """Predict marks for multiple study hours values."""
    model = get_model()
    predictions = model.predict([[h] for h in study_hours_list])
    return [
        {"study_hours": h, "predicted_marks": round(p, 2)}
        for h, p in zip(study_hours_list, predictions)
    ]


def get_metrics() -> dict:
    """Get model evaluation metrics."""
    global _metrics
    if _metrics is not None:
        return _metrics

    model = get_model()
    df = load_dataset()
    X = df[["Study_Hours"]].values
    y = df["Marks"].values
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    y_pred = model.predict(X_test)

    slope = model.coef_[0]
    intercept = model.intercept_
    r2 = r2_score(y_test, y_pred)

    _metrics = {
        "mae": round(mean_absolute_error(y_test, y_pred), 4),
        "mse": round(mean_squared_error(y_test, y_pred), 4),
        "rmse": round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 4),
        "r2_score": round(r2, 4),
        "confidence": round(r2 * 100, 2),
        "equation": f"Marks = {slope:.2f} * Study_Hours + {intercept:.2f}",
        "training_samples": int(len(X) * 0.8),
        "testing_samples": int(len(X_test)),
    }
    return _metrics


def get_chart_data() -> dict:
    """Generate chart data as base64-encoded images."""
    model = get_model()
    df = load_dataset()
    X = df[["Study_Hours"]].values
    y = df["Marks"].values
    y_pred_all = model.predict(X)

    # Scatter plot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(X, y, color="steelblue", alpha=0.7, edgecolors="white", s=60)
    ax.set_title("Study Hours vs Marks", fontsize=14, fontweight="bold")
    ax.set_xlabel("Study Hours")
    ax.set_ylabel("Marks")
    ax.grid(True, alpha=0.3)
    scatter_b64 = _fig_to_base64(fig)
    plt.close(fig)

    # Regression line
    fig, ax = plt.subplots(figsize=(8, 5))
    sort_idx = np.argsort(X.flatten())
    ax.scatter(X, y, color="steelblue", alpha=0.7, edgecolors="white", s=60, label="Actual")
    ax.plot(X.flatten()[sort_idx], y_pred_all[sort_idx], color="red", linewidth=2, label="Regression Line")
    ax.set_title("Linear Regression Fit", fontsize=14, fontweight="bold")
    ax.set_xlabel("Study Hours")
    ax.set_ylabel("Marks")
    ax.legend()
    ax.grid(True, alpha=0.3)
    regression_b64 = _fig_to_base64(fig)
    plt.close(fig)

    # Histogram
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].hist(df["Study_Hours"], bins=15, color="steelblue", edgecolor="white", alpha=0.8)
    axes[0].set_title("Study Hours Distribution")
    axes[0].set_xlabel("Study Hours")
    axes[0].set_ylabel("Frequency")
    axes[0].grid(True, alpha=0.3)
    axes[1].hist(df["Marks"], bins=15, color="coral", edgecolor="white", alpha=0.8)
    axes[1].set_title("Marks Distribution")
    axes[1].set_xlabel("Marks")
    axes[1].set_ylabel("Frequency")
    axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    histogram_b64 = _fig_to_base64(fig)
    plt.close(fig)

    return {
        "scatter": {"image": scatter_b64, "title": "Study Hours vs Marks"},
        "regression": {"image": regression_b64, "title": "Linear Regression Fit"},
        "histogram": {"image": histogram_b64, "title": "Feature Distributions"},
    }


def retrain_model() -> dict:
    """Retrain the model and return new metrics."""
    global _model, _metrics

    old_metrics = get_metrics() if _model is not None else None

    df = load_dataset()
    X = df[["Study_Hours"]].values
    y = df["Marks"].values

    # Preprocessing
    df_clean = df.drop_duplicates()
    X = df_clean[["Study_Hours"]].values
    y = df_clean["Marks"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    # Update cache
    _model = model
    _metrics = None  # Force recalculation

    new_metrics = get_metrics()
    new_metrics["old_metrics"] = old_metrics

    return new_metrics


def _fig_to_base64(fig) -> str:
    """Convert matplotlib figure to base64 string."""
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")
