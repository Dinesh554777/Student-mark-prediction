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

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "marks_model.pkl")
MULTI_MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "multi_feature_model.pkl")
DATASET_PATH = os.path.join(PROJECT_ROOT, "dataset", "student_marks.csv")

_model = None
_multi_model = None
_metrics = None
_chart_cache = None


def get_model():
    """Load or return cached single-feature model."""
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Train first.")
        _model = joblib.load(MODEL_PATH)
    return _model


def get_multi_model():
    """Load or return cached multi-feature model."""
    global _multi_model
    if _multi_model is None:
        if os.path.exists(MULTI_MODEL_PATH):
            _multi_model = joblib.load(MULTI_MODEL_PATH)
    return _multi_model


def invalidate_model_cache():
    """Force model reload on next access."""
    global _model, _multi_model, _metrics, _chart_cache
    _model = None
    _multi_model = None
    _metrics = None
    _chart_cache = None


def load_dataset():
    """Load the student marks dataset."""
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")
    return pd.read_csv(DATASET_PATH)


def _build_multi_feature_dataset():
    """Build a multi-feature dataset from the base dataset."""
    df = load_dataset()
    np.random.seed(42)
    n = len(df)
    df["Attendance"] = np.clip(50 + 5 * df["Study_Hours"] + np.random.normal(0, 10, n), 20, 100).round(1)
    df["Sleep_Hours"] = np.clip(7 + np.random.normal(0, 1.5, n), 3, 12).round(1)
    df["Previous_Score"] = np.clip(df["Marks"] + np.random.normal(0, 5, n), 5, 100).round(1)
    return df


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


def predict_multi(study_hours: float, attendance: float = 0,
                  sleep_hours: float = 0, previous_score: float = 0) -> dict:
    """Predict marks using multi-feature model."""
    multi_model = get_multi_model()
    if multi_model is None:
        result = predict(study_hours)
        result["features_used"] = ["Study_Hours"]
        return result

    features = [[study_hours, attendance, sleep_hours, previous_score]]
    prediction = multi_model.predict(features)[0]
    coefs = multi_model.coef_
    intercept = multi_model.intercept_

    feature_names = ["Study_Hours", "Attendance", "Sleep_Hours", "Previous_Score"]
    terms = [f"{coefs[i]:.2f} * {feature_names[i]}" for i in range(len(coefs))]
    equation = f"Marks = {' + '.join(terms)} + {intercept:.2f}"

    return {
        "study_hours": study_hours,
        "predicted_marks": round(prediction, 2),
        "equation": equation,
        "features_used": feature_names,
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


def get_recharts_data() -> dict:
    """Get chart data formatted for Recharts."""
    model = get_model()
    df = load_dataset()
    X = df["Study_Hours"].values
    y = df["Marks"].values
    y_pred = model.predict(X.reshape(-1, 1))

    # Scatter data
    scatter = [{"x": round(float(x), 1), "y": round(float(y_), 1)}
               for x, y_ in zip(X, y)]

    # Regression line
    sort_idx = np.argsort(X)
    regression_line = [{"x": round(float(X[i]), 1), "y": round(float(y_pred[i]), 1)}
                       for i in sort_idx]

    # Histograms
    study_bins = np.histogram(X, bins=15)
    marks_bins = np.histogram(y, bins=15)

    study_dist = [{"name": f"{study_bins[1][i]:.1f}-{study_bins[1][i+1]:.1f}",
                   "value": int(study_bins[0][i])}
                  for i in range(len(study_bins[0]))]

    marks_dist = [{"name": f"{marks_bins[1][i]:.0f}-{marks_bins[1][i+1]:.0f}",
                   "value": int(marks_bins[0][i])}
                  for i in range(len(marks_bins[0]))]

    return {
        "scatter": scatter,
        "regression_line": regression_line,
        "study_hours_dist": study_dist,
        "marks_dist": marks_dist,
    }


def get_chart_data() -> dict:
    """Generate chart data as base64-encoded images (cached)."""
    global _chart_cache
    if _chart_cache is not None:
        return _chart_cache

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

    _chart_cache = {
        "scatter": {"image": scatter_b64, "title": "Study Hours vs Marks"},
        "regression": {"image": regression_b64, "title": "Linear Regression Fit"},
        "histogram": {"image": histogram_b64, "title": "Feature Distributions"},
    }
    return _chart_cache


def train_multi_feature_model() -> dict:
    """Train and save the multi-feature model."""
    global _multi_model

    df = _build_multi_feature_dataset()
    features = ["Study_Hours", "Attendance", "Sleep_Hours", "Previous_Score"]
    X = df[features].values
    y = df["Marks"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    os.makedirs(os.path.dirname(MULTI_MODEL_PATH), exist_ok=True)
    joblib.dump(model, MULTI_MODEL_PATH)
    _multi_model = model

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    return {
        "r2_score": round(r2, 4),
        "mae": round(mean_absolute_error(y_test, y_pred), 4),
        "rmse": round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 4),
        "features": features,
        "coefficients": {f: round(float(c), 4) for f, c in zip(features, model.coef_)},
        "intercept": round(float(model.intercept_), 4),
    }


def retrain_model() -> dict:
    """Retrain the model and return new metrics."""
    global _model, _metrics, _chart_cache

    old_metrics = get_metrics() if _model is not None else None

    df = load_dataset()
    X = df[["Study_Hours"]].values
    y = df["Marks"].values

    df_clean = df.drop_duplicates()
    X = df_clean[["Study_Hours"]].values
    y = df_clean["Marks"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    _model = model
    _metrics = None
    _chart_cache = None

    new_metrics = get_metrics()
    new_metrics["old_metrics"] = old_metrics

    return new_metrics


def _fig_to_base64(fig) -> str:
    """Convert matplotlib figure to base64 string."""
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")
