"""Model training module for Student Marks Prediction.

Handles Linear Regression model training, evaluation, and saving.
"""

import os
import numpy as np
import joblib
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.data_preprocessing import preprocess_data, split_train_test
from src.utils import load_dataset, save_evaluation_metrics, ensure_directories


def train_linear_regression(X_train, y_train):
    """Train a Linear Regression model.

    Args:
        X_train: Training features.
        y_train: Training target.

    Returns:
        LinearRegression: Trained model.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("\nModel trained successfully!")
    print(f"  Coefficient (slope): {model.coef_[0]:.4f}")
    print(f"  Intercept: {model.intercept_:.4f}")
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate the trained model on test data.

    Args:
        model: Trained model.
        X_test: Test features.
        y_test: Test target.

    Returns:
        dict: Evaluation metrics.
    """
    y_pred = model.predict(X_test)

    metrics = {
        "MAE (Mean Absolute Error)": mean_absolute_error(y_test, y_pred),
        "MSE (Mean Squared Error)": mean_squared_error(y_test, y_pred),
        "RMSE (Root Mean Squared Error)": np.sqrt(mean_squared_error(y_test, y_pred)),
        "R2 Score": r2_score(y_test, y_pred),
    }

    print("\n--- Model Evaluation ---")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")

    # Calculate prediction confidence (R2 as percentage)
    confidence = r2_score(y_test, y_pred) * 100
    print(f"\n  Prediction Confidence: {confidence:.2f}%")

    # Display regression equation
    slope = model.coef_[0]
    intercept = model.intercept_
    print(f"\n  Regression Equation: Marks = {slope:.2f} * Study_Hours + {intercept:.2f}")

    return metrics, y_pred


def save_model(model, filepath="models/marks_model.pkl"):
    """Save the trained model to disk.

    Args:
        model: Trained model object.
        filepath (str): Path to save the model.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)
    print(f"\nModel saved to {filepath}")


def plot_scatter(X, y, filepath="outputs/scatter_plot.png"):
    """Create and save a scatter plot of the data.

    Args:
        X: Feature data.
        y: Target data.
        filepath (str): Path to save the plot.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.scatter(X, y, color="steelblue", alpha=0.7, edgecolors="white", s=60)
    plt.title("Study Hours vs Marks", fontsize=14, fontweight="bold")
    plt.xlabel("Study Hours", fontsize=12)
    plt.ylabel("Marks", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"Scatter plot saved to {filepath}")


def plot_regression_line(model, X, y, filepath="outputs/regression_line.png"):
    """Create and save a plot with the regression line.

    Args:
        model: Trained model.
        X: Feature data.
        y: Target data.
        filepath (str): Path to save the plot.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    y_pred_line = model.predict(X)

    plt.figure(figsize=(8, 6))
    plt.scatter(X, y, color="steelblue", alpha=0.7, edgecolors="white", s=60, label="Actual")
    plt.plot(sorted(X.flatten()), [y_pred_line[i] for i in np.argsort(X.flatten())],
             color="red", linewidth=2, label="Regression Line")
    plt.title("Linear Regression Fit", fontsize=14, fontweight="bold")
    plt.xlabel("Study Hours", fontsize=12)
    plt.ylabel("Marks", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"Regression line plot saved to {filepath}")


def plot_histogram(df, filepath="outputs/histogram.png"):
    """Create and save histograms of the features.

    Args:
        df: Dataset DataFrame.
        filepath (str): Path to save the plot.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].hist(df["Study_Hours"], bins=15, color="steelblue", edgecolor="white", alpha=0.8)
    axes[0].set_title("Distribution of Study Hours", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Study Hours")
    axes[0].set_ylabel("Frequency")
    axes[0].grid(True, alpha=0.3)

    axes[1].hist(df["Marks"], bins=15, color="coral", edgecolor="white", alpha=0.8)
    axes[1].set_title("Distribution of Marks", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Marks")
    axes[1].set_ylabel("Frequency")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"Histogram saved to {filepath}")


def plot_boxplot(df, filepath="outputs/boxplot.png"):
    """Create and save box plots of the features.

    Args:
        df: Dataset DataFrame.
        filepath (str): Path to save the plot.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].boxplot(df["Study_Hours"], patch_artist=True,
                    boxprops=dict(facecolor="steelblue", alpha=0.7))
    axes[0].set_title("Study Hours", fontsize=12, fontweight="bold")
    axes[0].set_ylabel("Hours")
    axes[0].grid(True, alpha=0.3)

    axes[1].boxplot(df["Marks"], patch_artist=True,
                    boxprops=dict(facecolor="coral", alpha=0.7))
    axes[1].set_title("Marks", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("Marks")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"Box plot saved to {filepath}")


def run_training_pipeline():
    """Execute the full training pipeline.

    Returns:
        tuple: (model, metrics) trained model and evaluation metrics.
    """
    ensure_directories()

    # Load and preprocess data
    df = load_dataset()
    X, y = preprocess_data(df)
    X_train, X_test, y_train, y_test = split_train_test(X, y)

    # Train model
    model = train_linear_regression(X_train, y_train)

    # Evaluate
    metrics, y_pred = evaluate_model(model, X_test, y_test)

    # Save model and metrics
    save_model(model)
    save_evaluation_metrics(metrics)

    # Generate plots
    plot_scatter(X, y)
    plot_regression_line(model, X, y)
    plot_histogram(df)
    plot_boxplot(df)

    # Training accuracy
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"\nTraining Accuracy (R2): {train_score:.4f}")
    print(f"Testing Accuracy (R2):  {test_score:.4f}")

    return model, metrics


if __name__ == "__main__":
    run_training_pipeline()
