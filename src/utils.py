"""Utility functions for the Student Marks Prediction project.

This module provides helper functions for file I/O, directory management,
and other common operations used across the project.
"""

import os
import numpy as np
import pandas as pd


def ensure_directories():
    """Create project directories if they don't exist."""
    dirs = ["dataset", "models", "outputs", "notebooks"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)


def generate_dataset(n_samples=100, save_path="dataset/student_marks.csv"):
    """Generate a realistic synthetic student marks dataset.

    Args:
        n_samples (int): Number of records to generate.
        save_path (str): Path to save the CSV file.
    """
    np.random.seed(42)
    study_hours = np.round(np.random.uniform(0.5, 10.0, n_samples), 1)

    # Realistic linear relationship with some noise
    # Marks = base + slope * hours + noise
    marks = 5 + 9.5 * study_hours + np.random.normal(0, 3, n_samples)
    marks = np.clip(marks, 5, 100).astype(int)

    df = pd.DataFrame({
        "Study_Hours": study_hours,
        "Marks": marks
    })

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"Dataset generated: {save_path} ({n_samples} records)")
    return df


def load_dataset(path="dataset/student_marks.csv"):
    """Load the student marks dataset.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    if not os.path.exists(path):
        print(f"Dataset not found at {path}. Generating...")
        generate_dataset(save_path=path)
    return pd.read_csv(path)


def display_dataset_info(df):
    """Display comprehensive dataset information.

    Args:
        df (pd.DataFrame): The dataset to analyze.
    """
    print("\n" + "=" * 50)
    print("DATASET INFORMATION")
    print("=" * 50)

    print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")

    print("\n--- First 5 Rows ---")
    print(df.head())

    print("\n--- Data Types ---")
    print(df.dtypes)

    print("\n--- Null Values ---")
    print(df.isnull().sum())

    print("\n--- Statistical Summary ---")
    print(df.describe())

    print("\n--- Correlation ---")
    print(df.corr())


def save_evaluation_metrics(metrics, filepath="outputs/evaluation.txt"):
    """Save model evaluation metrics to a text file.

    Args:
        dict: Dictionary containing evaluation metrics.
        filepath (str): Path to save the evaluation results.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("=" * 50 + "\n")
        f.write("MODEL EVALUATION RESULTS\n")
        f.write("=" * 50 + "\n\n")
        for key, value in metrics.items():
            f.write(f"{key}: {value:.4f}\n")
        f.write("\n" + "=" * 50 + "\n")
    print(f"Evaluation metrics saved to {filepath}")


if __name__ == "__main__":
    ensure_directories()
    df = generate_dataset()
    display_dataset_info(df)
