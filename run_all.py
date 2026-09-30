"""
Master Runner for the Customer Churn Data Science Project.
Executes the full lifecycle:
1. Synthetic Data Generation
2. Machine Learning Training & Model Selection
3. Evaluation Metrics & Visualizations
4. Real-time Inference Demonstration
"""

import sys
import time
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from data_generator import generate_customer_data
from train_and_evaluate import run_pipeline
from predict import run_sample_predictions

def main():
    start_time = time.time()
    print("\n" + "=" * 65)
    print(">> STARTING DATA SCIENCE PROJECT EXECUTION")
    print("=" * 65)

    # 1. Dataset Generation
    print("\n[Step 1/3] Generating Clean Dataset...")
    data_dir = BASE_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    df = generate_customer_data(n_samples=1200)
    csv_file = data_dir / "customers.csv"
    df.to_csv(csv_file, index=False)
    print(f"-> Generated {len(df)} samples saved to {csv_file}")

    # 2. Model Training & Evaluation
    print("\n[Step 2/3] Training & Benchmarking ML Classifiers...")
    run_pipeline()

    # 3. Inference
    print("\n[Step 3/3] Running Inference on Test Customer Profiles...")
    run_sample_predictions()

    elapsed = round(time.time() - start_time, 2)
    print("\n" + "=" * 65)
    print(f">> ALL STEPS COMPLETED SUCCESSFULLY IN {elapsed} SECONDS!")
    print("=" * 65)
    print(f"Artifacts Generated:")
    print(f"  * Dataset:               {csv_file}")
    print(f"  * Serialized Model:      {BASE_DIR / 'outputs' / 'best_model.joblib'}")
    print(f"  * Evaluation Charts:     {BASE_DIR / 'outputs' / 'evaluation_dashboard.png'}")
    print(f"  * Classification Report: {BASE_DIR / 'outputs' / 'classification_report.txt'}")
    print("\nOptional Web App:")
    print("  Run 'python churn_predictor/app.py' to launch the interactive UI on http://127.0.0.1:5000\n")

if __name__ == "__main__":
    main()
