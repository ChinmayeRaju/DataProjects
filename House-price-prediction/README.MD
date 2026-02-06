# 🏠 House Price Prediction – California Housing (Neural Network)

This project uses a fully connected neural network (TensorFlow/Keras) to predict **California house prices** from the classic **California Housing** dataset, built and run inside a **Python virtual environment**.

Main work is in the Jupyter notebook:

> `notebooks/HousePrediction.ipynb`  
> (or `HousePrediction.ipynb` in your project root, depending on how you organized it)

---

## ✨ What This Project Does

- Loads the **California Housing dataset** from `sklearn.datasets.fetch_california_housing`
- Combines features and target into a single pandas DataFrame
- Performs basic **Exploratory Data Analysis (EDA)**:
  - Prints dataset shape
  - Shows first rows
  - Uses `describe()` for basic statistics
  - Checks for missing values
- Splits data into **train, validation, and test** sets
- Scales features using **StandardScaler**
- Builds a **neural network regression model** in TensorFlow/Keras
- Trains the model and evaluates it using **MSE, MAE, and R²**
- Visualizes training behavior and prediction quality

---

## 🧱 Tech Stack

- **Python:** 3.11 (inside virtual environment)
- **Deep Learning:** TensorFlow / Keras
- **ML Utilities:** scikit-learn
- **Data Handling:** pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Interface:** Jupyter Notebook
- **Env Management:** `venv` (virtual environment)

---

## 📂 Project Structure (example)

```text
House-price-prediction/
├── .venv/                      # Python virtual environment (ignored by git)
├── HousePrediction.ipynb       # Main notebook for this project
├── requirements.txt            # Python dependencies
└── README.md                   # This file
