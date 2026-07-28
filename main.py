"""Student Marks Prediction - Main Program.

A machine learning project that predicts student exam marks
based on study hours using Linear Regression.
"""

import sys
from src.utils import load_dataset, display_dataset_info, ensure_directories
from src.train_model import run_training_pipeline
from src.predict import interactive_predict, predict_from_csv


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 40)
    print("   STUDENT MARKS PREDICTION")
    print("=" * 40)
    print("  1. Train Model")
    print("  2. Predict Marks")
    print("  3. Predict from CSV")
    print("  4. Show Dataset Info")
    print("  5. Exit")
    print("=" * 40)


def main():
    """Main entry point for the application."""
    ensure_directories()

    while True:
        display_menu()
        choice = input("\n  Enter your choice (1-5): ").strip()

        if choice == "1":
            print("\n--- Training Model ---")
            try:
                run_training_pipeline()
                print("\nTraining completed successfully!")
            except Exception as e:
                print(f"\nError during training: {e}")

        elif choice == "2":
            interactive_predict()

        elif choice == "3":
            csv_path = input("\nEnter CSV file path: ").strip()
            try:
                results = predict_from_csv(csv_path, "outputs/predictions.csv")
                print("\n--- Predictions ---")
                print(results.to_string(index=False))
            except Exception as e:
                print(f"\nError: {e}")

        elif choice == "4":
            df = load_dataset()
            display_dataset_info(df)

        elif choice == "5":
            print("\nThank you for using Student Marks Prediction!")
            sys.exit(0)

        else:
            print("\nInvalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
