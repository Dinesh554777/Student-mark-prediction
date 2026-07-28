"""Data preprocessing module for Student Marks Prediction.

Handles data cleaning, splitting, and preparation for model training.
"""

import pandas as pd
from sklearn.model_selection import train_test_split


def preprocess_data(df):
    """Preprocess the dataset for model training.

    Steps:
        - Check and handle missing values
        - Remove duplicate rows
        - Split features (X) and target (y)

    Args:
        df (pd.DataFrame): Raw dataset.

    Returns:
        tuple: (X, y) features and target arrays.
    """
    print("\n--- Data Preprocessing ---")

    # Check missing values
    missing = df.isnull().sum().sum()
    if missing > 0:
        print(f"Found {missing} missing values. Filling with mean...")
        df = df.fillna(df.mean())
    else:
        print("No missing values found.")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    if before != after:
        print(f"Removed {before - after} duplicate rows.")
    else:
        print("No duplicate rows found.")

    # Split features and target
    X = df[["Study_Hours"]].values
    y = df["Marks"].values
    print(f"Features shape: {X.shape}, Target shape: {y.shape}")

    return X, y


def split_train_test(X, y, test_size=0.2, random_state=42):
    """Split data into training and testing sets.

    Args:
        X: Feature matrix.
        y: Target vector.
        test_size (float): Proportion of data for testing.
        random_state (int): Random seed for reproducibility.

    Returns:
        tuple: X_train, X_test, y_train, y_test
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"\nTrain set: {X_train.shape[0]} samples")
    print(f"Test set:  {X_test.shape[0]} samples")
    return X_train, X_test, y_train, y_test
