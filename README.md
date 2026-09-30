# 🎯 Customer Churn Prediction & Risk Intelligence System

A lightweight, end-to-end Data Science & Machine Learning project designed for **speed, minimal resource consumption (< 150 MB RAM, runs in ~2 seconds on CPU)**, and real-world business value.

---

## 🚀 Key Highlights
- **Zero Heavy Dependencies**: Uses standard lightweight libraries (`pandas`, `scikit-learn`, `matplotlib`, `Flask`).
- **Complete DS Lifecycle**:
  1. Data generation & cleaning
  2. Exploratory Data Analysis & Preprocessing Pipeline
  3. Benchmarking 3 ML Classifiers (Logistic Regression, Random Forest, Gradient Boosting)
  4. Model serialization (`.joblib`)
  5. Multi-metric evaluation (Confusion Matrix, ROC curves, Feature Importances)
  6. Real-time Inference Engine & Business Recommendation Generator
  7. Interactive Web App for demos & testing

---

## 📁 Project Structure

```text
churn_predictor/
│── data/
│   └── customers.csv               # Clean tabular dataset (1,200 rows)
│── outputs/
│   ├── best_model.joblib           # Serialized champion ML model
│   ├── evaluation_dashboard.png    # 4-panel visual performance chart
│   └── classification_report.txt   # Precision, recall, and F1 summary
│── data_generator.py               # Self-contained data generator
│── train_and_evaluate.py           # Training, cross-validation & evaluation
│── predict.py                      # Risk assessment & inference engine
│── app.py                          # Modern interactive web dashboard (Flask)
│── run_all.py                      # 1-Click master runner script
└── README.md                       # Project documentation
```

---

## ⚡ How to Run

### 1. Run the Entire Pipeline (Runs in ~2 seconds)
```bash
python churn_predictor/run_all.py
```

### 2. Run Real-time Predictions Only
```bash
python churn_predictor/predict.py
```

### 3. Launch the Interactive Web Dashboard
```bash
python churn_predictor/app.py
```
Then open your browser at: `http://127.0.0.1:5000`

---

## 📊 Model Evaluation Summary

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Champion)** | **76.7%** | **71.4%** | **50.0%** | **0.588** | **0.797** |
| Random Forest | 74.2% | 70.5% | 38.8% | 0.500 | 0.761 |
| Gradient Boosting | 72.9% | 60.9% | 52.5% | 0.564 | 0.760 |

### Top Drivers of Churn:
1. **Contract Type**: Month-to-Month contracts have significantly higher churn probability.
2. **Tenure Months**: Newer customers (< 6 months) show the highest attrition risk.
3. **Monthly Charges & Tech Support**: High fees without active tech support trigger churn.
