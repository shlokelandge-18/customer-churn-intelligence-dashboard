"""
Dataset Generator for Customer Churn Prediction.
Generates realistic, clean tabular customer data with zero external downloads.
"""

import numpy as np
import pandas as pd
from pathlib import Path

def generate_customer_data(n_samples: int = 1200, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    
    customer_ids = [f"CUST-{1000 + i}" for i in range(n_samples)]
    age = np.random.randint(18, 70, size=n_samples)
    tenure_months = np.random.randint(1, 72, size=n_samples)
    contract = np.random.choice(["Month-to-month", "One year", "Two year"], size=n_samples, p=[0.55, 0.25, 0.20])
    internet_service = np.random.choice(["Fiber optic", "DSL", "No"], size=n_samples, p=[0.45, 0.35, 0.20])
    tech_support = np.random.choice(["Yes", "No"], size=n_samples, p=[0.35, 0.65])
    online_security = np.random.choice(["Yes", "No"], size=n_samples, p=[0.30, 0.70])
    paperless_billing = np.random.choice(["Yes", "No"], size=n_samples, p=[0.60, 0.40])
    payment_method = np.random.choice(
        ["Electronic check", "Mailed check", "Bank transfer", "Credit card"],
        size=n_samples,
        p=[0.35, 0.20, 0.25, 0.20]
    )

    # Base monthly charges depending on internet service
    monthly_base = np.where(internet_service == "Fiber optic", 85.0, 
                    np.where(internet_service == "DSL", 55.0, 25.0))
    monthly_charges = np.round(monthly_base + np.random.uniform(-10, 15, size=n_samples), 2)
    monthly_charges = np.clip(monthly_charges, 18.0, 120.0)

    # Total charges approx tenure * monthly charges with slight noise
    total_charges = np.round(tenure_months * monthly_charges * np.random.uniform(0.95, 1.05, size=n_samples), 2)

    # Realistic Churn probability log-odds calculation
    log_odds = (
        -1.2
        + (monthly_charges / 50.0) * 0.7
        - (tenure_months / 24.0) * 1.1
        + np.where(contract == "Month-to-month", 1.2, np.where(contract == "One year", -0.3, -1.0))
        + np.where(tech_support == "No", 0.6, -0.4)
        + np.where(online_security == "No", 0.5, -0.3)
        + np.where(payment_method == "Electronic check", 0.4, -0.1)
    )
    
    # Sigmoid function for probability
    probs = 1 / (1 + np.exp(-log_odds))
    churn = (np.random.rand(n_samples) < probs).astype(int)

    df = pd.DataFrame({
        "CustomerID": customer_ids,
        "Age": age,
        "TenureMonths": tenure_months,
        "Contract": contract,
        "InternetService": internet_service,
        "TechSupport": tech_support,
        "OnlineSecurity": online_security,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "Churn": churn
    })

    return df

if __name__ == "__main__":
    output_dir = Path(__file__).parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "customers.csv"
    
    df = generate_customer_data()
    df.to_csv(csv_path, index=False)
    print(f"[+] Successfully generated {len(df)} customer records at: {csv_path}")
    print(f"[i] Churn distribution:\n{df['Churn'].value_counts(normalize=True).round(3) * 100}%")
