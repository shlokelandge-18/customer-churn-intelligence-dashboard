"""
Model Training, Cross-Validation, Evaluation, and Visualization Pipeline.
Lightweight, executes in seconds on standard CPU.
"""

from pathlib import Path
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def run_pipeline():
    base_dir = Path(__file__).parent
    data_path = base_dir / "data" / "customers.csv"
    outputs_dir = base_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        from data_generator import generate_customer_data
        df = generate_customer_data()
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)

    print("=" * 65)
    print("      CUSTOMER CHURN PREDICTION PIPELINE (LIGHTWEIGHT ML)      ")
    print("=" * 65)
    print(f"[*] Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"[*] Target Variable: Churn (1 = Left, 0 = Retained)")
    print(f"[*] Class Balance: {df['Churn'].mean() * 100:.1f}% positive churn rate\n")

    # Features and Target
    feature_cols = [
        "Age", "TenureMonths", "Contract", "InternetService",
        "TechSupport", "OnlineSecurity", "PaperlessBilling",
        "PaymentMethod", "MonthlyCharges", "TotalCharges"
    ]
    X = df[feature_cols]
    y = df["Churn"]

    numerical_features = ["Age", "TenureMonths", "MonthlyCharges", "TotalCharges"]
    categorical_features = [
        "Contract", "InternetService", "TechSupport",
        "OnlineSecurity", "PaperlessBilling", "PaymentMethod"
    ]

    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), categorical_features),
        ]
    )

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"[*] Training samples: {len(X_train)} | Test samples: {len(X_test)}")

    # Candidate Models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
    }

    results = []
    trained_pipelines = {}
    test_predictions = {}
    test_probabilities = {}

    print("\n--- Model Benchmarking ---")
    for name, clf in models.items():
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        
        # Train
        pipeline.fit(X_train, y_train)
        trained_pipelines[name] = pipeline

        # Predict
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]

        test_predictions[name] = y_pred
        test_probabilities[name] = y_prob

        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)

        results.append({
            "Model": name,
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1-Score": f1,
            "ROC-AUC": roc_auc
        })
        print(f"[{name}] Acc: {acc:.3f} | F1: {f1:.3f} | ROC-AUC: {roc_auc:.3f}")

    results_df = pd.DataFrame(results).sort_values(by="ROC-AUC", ascending=False)
    print("\n" + results_df.to_string(index=False))

    best_model_name = results_df.iloc[0]["Model"]
    best_pipeline = trained_pipelines[best_model_name]
    print(f"\n[+] Champion Model Selected: {best_model_name}")

    # Save champion model
    model_save_path = outputs_dir / "best_model.joblib"
    joblib.dump(best_pipeline, model_save_path)
    print(f"[+] Saved serialized model to: {model_save_path}")

    # Generate Visualization Dashboard
    print("[*] Generating Performance Visualizations...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Customer Churn Data Science Performance Dashboard", fontsize=16, fontweight="bold")

    # Plot 1: Model Comparison Bar Chart
    ax1 = axes[0, 0]
    x_indices = np.arange(len(results_df))
    bar_width = 0.35
    ax1.bar(x_indices - bar_width/2, results_df["F1-Score"], width=bar_width, label="F1-Score", color="#4C72B0")
    ax1.bar(x_indices + bar_width/2, results_df["ROC-AUC"], width=bar_width, label="ROC-AUC", color="#55A868")
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(results_df["Model"], rotation=15, ha="right")
    ax1.set_ylim(0.5, 1.0)
    ax1.set_ylabel("Score")
    ax1.set_title("Model Comparison (F1 vs ROC-AUC)")
    ax1.legend(loc="lower right")
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    # Plot 2: Confusion Matrix of Best Model
    ax2 = axes[0, 1]
    cm = confusion_matrix(y_test, test_predictions[best_model_name])
    im = ax2.imshow(cm, interpolation="nearest", cmap="Blues")
    ax2.set_title(f"Confusion Matrix ({best_model_name})")
    fig.colorbar(im, ax=ax2)
    classes = ["Retained (0)", "Churned (1)"]
    tick_marks = np.arange(len(classes))
    ax2.set_xticks(tick_marks)
    ax2.set_xticklabels(classes)
    ax2.set_yticks(tick_marks)
    ax2.set_yticklabels(classes)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax2.text(j, i, format(cm[i, j], "d"),
                     ha="center", va="center",
                     color="white" if cm[i, j] > cm.max() / 2.0 else "black",
                     fontsize=12, fontweight="bold")
    ax2.set_ylabel("Actual")
    ax2.set_xlabel("Predicted")

    # Plot 3: ROC Curves
    ax3 = axes[1, 0]
    for name in models.keys():
        fpr, tpr, _ = roc_curve(y_test, test_probabilities[name])
        auc_val = roc_auc_score(y_test, test_probabilities[name])
        ax3.plot(fpr, tpr, label=f"{name} (AUC = {auc_val:.3f})", lw=2)
    ax3.plot([0, 1], [0, 1], "k--", lw=1.5, label="Random Guess (0.50)")
    ax3.set_xlim([0.0, 1.0])
    ax3.set_ylim([0.0, 1.05])
    ax3.set_xlabel("False Positive Rate")
    ax3.set_ylabel("True Positive Rate")
    ax3.set_title("Receiver Operating Characteristic (ROC) Curves")
    ax3.legend(loc="lower right")
    ax3.grid(linestyle="--", alpha=0.7)

    # Plot 4: Feature Importance / Weights of Best Model
    ax4 = axes[1, 1]
    feature_names = (
        numerical_features + 
        list(best_pipeline.named_steps["preprocessor"].named_transformers_["cat"].get_feature_names_out(categorical_features))
    )
    
    clf_obj = best_pipeline.named_steps["classifier"]
    if hasattr(clf_obj, "feature_importances_"):
        importances = clf_obj.feature_importances_
        title_suffix = "Feature Importances"
    elif hasattr(clf_obj, "coef_"):
        importances = np.abs(clf_obj.coef_[0])
        title_suffix = "Absolute Coefficients"
    else:
        importances = np.ones(len(feature_names))
        title_suffix = "Features"

    sorted_idx = np.argsort(importances)[-10:]
    ax4.barh(np.array(feature_names)[sorted_idx], importances[sorted_idx], color="#C44E52")
    ax4.set_title(f"Top 10 Drivers of Churn ({title_suffix})")
    ax4.set_xlabel("Importance Weight")
    ax4.grid(axis="x", linestyle="--", alpha=0.7)

    plt.tight_layout()
    chart_path = outputs_dir / "evaluation_dashboard.png"
    plt.savefig(chart_path, dpi=180)
    plt.close()
    print(f"[+] Saved evaluation dashboard plot to: {chart_path}")

    # Save summary report text
    report_text = classification_report(y_test, test_predictions[best_model_name], target_names=["Retained", "Churned"])
    summary_report_path = outputs_dir / "classification_report.txt"
    with open(summary_report_path, "w") as f:
        f.write(f"CHAMPION MODEL: {best_model_name}\n")
        f.write("=" * 40 + "\n\n")
        f.write(report_text)
    print(f"[+] Detailed classification report written to: {summary_report_path}")
    print("\nPipeline execution complete successfully!")

if __name__ == "__main__":
    run_pipeline()
