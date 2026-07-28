# Student Marks Prediction

A Machine Learning project that predicts student exam marks based on the number of study hours using **Linear Regression**.

## Objectives

- Predict a student's marks based on their study hours
- Perform exploratory data analysis (EDA) on the dataset
- Visualize data patterns and regression fit
- Evaluate model performance using standard metrics
- Provide an interactive prediction interface

## Technologies Used

| Technology   | Purpose                  |
|--------------|--------------------------|
| Python 3.x   | Programming Language     |
| Pandas       | Data Manipulation        |
| NumPy        | Numerical Computing      |
| Matplotlib   | Data Visualization       |
| Scikit-learn | Machine Learning         |
| Joblib       | Model Serialization      |

## Folder Structure

```
Student-Marks-Prediction/
│
├── dataset/
│   └── student_marks.csv          # Generated dataset
│
├── notebooks/
│   └── EDA.ipynb                  # Exploratory Data Analysis
│
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py      # Data cleaning & splitting
│   ├── train_model.py             # Model training & evaluation
│   ├── predict.py                 # Prediction functions
│   └── utils.py                   # Utility functions
│
├── models/
│   └── marks_model.pkl            # Saved trained model
│
├── outputs/
│   ├── scatter_plot.png           # Data scatter plot
│   ├── regression_line.png        # Regression fit plot
│   ├── histogram.png              # Feature distributions
│   ├── boxplot.png                # Box plots
│   └── evaluation.txt             # Model metrics
│
├── requirements.txt
├── README.md
└── main.py                        # Main entry point
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/Student-Marks-Prediction.git
cd Student-Marks-Prediction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

### Train and use via menu:
```bash
python main.py
```

### Train directly:
```bash
python -m src.train_model
```

### Predict interactively:
```bash
python -m src.predict
```

## Dataset Description

| Column      | Description                          |
|-------------|--------------------------------------|
| Study_Hours | Number of hours a student studied    |
| Marks       | Exam marks obtained (0-100)          |

The dataset is auto-generated with 100 realistic records following a linear relationship with added noise.

## Algorithm

**Linear Regression** is used because:
- The relationship between study hours and marks is approximately linear
- It is simple, interpretable, and effective for single-feature prediction
- Provides a clear regression equation: `Marks = slope * Study_Hours + intercept`

## Results

After training, the model achieves:
- **R² Score** > 0.90 (high accuracy)
- **MAE** < 3 marks (low average error)
- **Prediction Confidence** > 90%

Detailed metrics are saved in `outputs/evaluation.txt`.

## Future Enhancements

- Add more features (attendance, sleep hours, previous scores)
- Try advanced algorithms (Random Forest, SVR, XGBoost)
- Build a Flask/Streamlit web application
- Add real-time prediction API
- Include student performance dashboard
- Support batch predictions from multiple files

## License

This project is for educational purposes.
