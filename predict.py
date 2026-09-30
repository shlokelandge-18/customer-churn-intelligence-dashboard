"""
Inference & Risk Scoring Engine.
Uses the trained champion model to provide real-time churn prediction,
risk tiers, and proactive retention actions.
"""

from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).parent / "outputs" / "best_model.joblib"

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please run train_and_evaluate.py first.")
    return joblib.load(MODEL_PATH)

def predict_single_customer(customer_data: dict, model=None):
    if model is None:
        model = load_model()
    
    df = pd.DataFrame([customer_data])
    prob = model.predict_proba(df)[0][1]
    prediction = int(prob >= 0.5)

    if prob < 0.35:
        risk_level = "LOW RISK"
        recommendation = "Standard retention. Account is stable."
        color_code = "GREEN"
    elif prob < 0.65:
        risk_level = "MODERATE RISK"
        recommendation = "Monitor activity. Offer contract loyalty discount or check-in call."
        color_code = "YELLOW"
    else:
        risk_level = "HIGH RISK"
        recommendation = "Immediate Intervention: Proactive outreach by Customer Success, offer 1-year contract discount + complimentary tech support."
        color_code = "RED"

    return {
        "churn_probability": round(prob * 100, 2),
        "prediction": "Will Churn" if prediction == 1 else "Will Stay",
        "risk_level": risk_level,
        "recommendation": recommendation,
        "flag": color_code
    }

def run_sample_predictions():
    print("=" * 65)
    print("      REAL-TIME CUSTOMER CHURN INFERENCE & RISK ENGINE         ")
    print("=" * 65)

    model = load_model()

    sample_customers = [
        {
            "name": "High Risk Profile (New Month-to-Month Customer, High Bill, No Support)",
            "data": {
                "Age": 28,
                "TenureMonths": 2,
                "Contract": "Month-to-month",
                "InternetService": "Fiber optic",
                "TechSupport": "No",
                "OnlineSecurity": "No",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 95.50,
                "TotalCharges": 191.00
            }
        },
        {
            "name": "Low Risk Profile (Loyal 2-Year Contract Customer with Support)",
            "data": {
                "Age": 54,
                "TenureMonths": 48,
                "Contract": "Two year",
                "InternetService": "DSL",
                "TechSupport": "Yes",
                "OnlineSecurity": "Yes",
                "PaperlessBilling": "No",
                "PaymentMethod": "Credit card",
                "MonthlyCharges": 58.20,
                "TotalCharges": 2793.60
            }
        },
        {
            "name": "Borderline / Moderate Risk Customer",
            "data": {
                "Age": 39,
                "TenureMonths": 14,
                "Contract": "One year",
                "InternetService": "Fiber optic",
                "TechSupport": "No",
                "OnlineSecurity": "Yes",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Bank transfer",
                "MonthlyCharges": 82.00,
                "TotalCharges": 1148.00
            }
        }
    ]

    for item in sample_customers:
        res = predict_single_customer(item["data"], model=model)
        print(f"\n>> Profile: {item['name']}")
        print(f"   Tenure: {item['data']['TenureMonths']} mos | Contract: {item['data']['Contract']} | Monthly: ${item['data']['MonthlyCharges']}")
        print(f"   Churn Probability: {res['churn_probability']}%")
        print(f"   Risk Tier:         [{res['risk_level']}]")
        print(f"   Action:            {res['recommendation']}")

if __name__ == "__main__":
    run_sample_predictions()
