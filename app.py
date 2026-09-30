"""
Lightweight Web Dashboard for Customer Churn Prediction.
Built with Flask (already available in the environment) + embedded responsive UI.
Run with: python app.py
"""

from flask import Flask, render_template_string, request, jsonify
from pathlib import Path
import joblib
import pandas as pd

app = Flask(__name__)
MODEL_PATH = Path(__file__).parent / "outputs" / "best_model.joblib"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Churn Intelligence Dashboard</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --high-risk: #ef4444;
            --mid-risk: #f59e0b;
            --low-risk: #10b981;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { background: var(--bg-color); color: var(--text-main); padding: 30px 15px; }
        .container { max-width: 900px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 30px; }
        header h1 { font-size: 2.2rem; color: #fff; margin-bottom: 8px; }
        header p { color: var(--text-muted); font-size: 1rem; }
        .badge { display: inline-block; background: rgba(56, 189, 248, 0.15); color: var(--accent); padding: 4px 12px; border-radius: 999px; font-size: 0.85rem; font-weight: 600; margin-bottom: 12px; }
        .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px; }
        .form-group { display: flex; flex-direction: column; }
        label { font-size: 0.85rem; font-weight: 600; color: var(--text-muted); margin-bottom: 6px; }
        input, select { background: #0b1120; border: 1px solid var(--border); border-radius: 6px; padding: 10px 12px; color: var(--text-main); font-size: 0.95rem; }
        input:focus, select:focus { outline: none; border-color: var(--accent); }
        button { background: linear-gradient(135deg, #0284c7, #2563eb); color: white; border: none; padding: 12px 24px; border-radius: 6px; font-size: 1rem; font-weight: 600; cursor: pointer; width: 100%; transition: opacity 0.2s; }
        button:hover { opacity: 0.9; }
        .result-box { display: none; margin-top: 20px; padding: 20px; border-radius: 8px; border: 1px solid var(--border); background: #0b1329; }
        .result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .score { font-size: 2rem; font-weight: 800; }
        .risk-pill { padding: 4px 12px; border-radius: 999px; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; }
        .advice { background: rgba(255,255,255,0.03); padding: 12px 16px; border-radius: 6px; font-size: 0.92rem; border-left: 3px solid var(--accent); }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <span class="badge">Lightweight Data Science ML App</span>
            <h1>Customer Churn Predictor</h1>
            <p>Predict customer retention risk in real-time using scikit-learn ML</p>
        </header>

        <div class="card">
            <form id="churnForm">
                <div class="grid">
                    <div class="form-group">
                        <label>Age</label>
                        <input type="number" id="Age" value="32" min="18" max="100" required>
                    </div>
                    <div class="form-group">
                        <label>Tenure (Months)</label>
                        <input type="number" id="TenureMonths" value="4" min="1" max="100" required>
                    </div>
                    <div class="form-group">
                        <label>Contract Type</label>
                        <select id="Contract">
                            <option value="Month-to-month">Month-to-month</option>
                            <option value="One year">One year</option>
                            <option value="Two year">Two year</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Internet Service</label>
                        <select id="InternetService">
                            <option value="Fiber optic">Fiber optic</option>
                            <option value="DSL">DSL</option>
                            <option value="No">No Internet</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Tech Support</label>
                        <select id="TechSupport">
                            <option value="No">No</option>
                            <option value="Yes">Yes</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Online Security</label>
                        <select id="OnlineSecurity">
                            <option value="No">No</option>
                            <option value="Yes">Yes</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Paperless Billing</label>
                        <select id="PaperlessBilling">
                            <option value="Yes">Yes</option>
                            <option value="No">No</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Payment Method</label>
                        <select id="PaymentMethod">
                            <option value="Electronic check">Electronic check</option>
                            <option value="Mailed check">Mailed check</option>
                            <option value="Bank transfer">Bank transfer</option>
                            <option value="Credit card">Credit card</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Monthly Charges ($)</label>
                        <input type="number" step="0.5" id="MonthlyCharges" value="89.5" required>
                    </div>
                    <div class="form-group">
                        <label>Total Charges ($)</label>
                        <input type="number" step="1.0" id="TotalCharges" value="358.0" required>
                    </div>
                </div>
                <button type="submit">Run Real-Time Prediction</button>
            </form>

            <div id="resultBox" class="result-box">
                <div class="result-header">
                    <div>
                        <span style="color: var(--text-muted); font-size: 0.85rem;">CHURN PROBABILITY</span>
                        <div id="scoreDisplay" class="score">0%</div>
                    </div>
                    <span id="riskBadge" class="risk-pill"></span>
                </div>
                <div class="advice">
                    <strong>Recommended Strategy:</strong>
                    <p id="recommendationText" style="margin-top: 4px; color: #cbd5e1;"></p>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('churnForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const data = {
                Age: parseInt(document.getElementById('Age').value),
                TenureMonths: parseInt(document.getElementById('TenureMonths').value),
                Contract: document.getElementById('Contract').value,
                InternetService: document.getElementById('InternetService').value,
                TechSupport: document.getElementById('TechSupport').value,
                OnlineSecurity: document.getElementById('OnlineSecurity').value,
                PaperlessBilling: document.getElementById('PaperlessBilling').value,
                PaymentMethod: document.getElementById('PaymentMethod').value,
                MonthlyCharges: parseFloat(document.getElementById('MonthlyCharges').value),
                TotalCharges: parseFloat(document.getElementById('TotalCharges').value)
            };

            const response = await fetch('/predict_api', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const res = await response.json();
            const resultBox = document.getElementById('resultBox');
            const scoreDisplay = document.getElementById('scoreDisplay');
            const riskBadge = document.getElementById('riskBadge');
            const recText = document.getElementById('recommendationText');

            resultBox.style.display = 'block';
            scoreDisplay.textContent = res.churn_probability + '%';
            recText.textContent = res.recommendation;

            if (res.flag === 'GREEN') {
                scoreDisplay.style.color = '#10b981';
                riskBadge.textContent = 'LOW RISK';
                riskBadge.style.backgroundColor = 'rgba(16, 185, 129, 0.2)';
                riskBadge.style.color = '#10b981';
            } else if (res.flag === 'YELLOW') {
                scoreDisplay.style.color = '#f59e0b';
                riskBadge.textContent = 'MODERATE RISK';
                riskBadge.style.backgroundColor = 'rgba(245, 158, 11, 0.2)';
                riskBadge.style.color = '#f59e0b';
            } else {
                scoreDisplay.style.color = '#ef4444';
                riskBadge.textContent = 'HIGH RISK';
                riskBadge.style.backgroundColor = 'rgba(239, 68, 68, 0.2)';
                riskBadge.style.color = '#ef4444';
            }
        });
    </script>
</body>
</html>
"""

model = None

def get_model():
    global model
    if model is None:
        if not MODEL_PATH.exists():
            from train_and_evaluate import run_pipeline
            run_pipeline()
        model = joblib.load(MODEL_PATH)
    return model

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/predict_api", methods=["POST"])
def predict_api():
    from predict import predict_single_customer
    data = request.get_json()
    res = predict_single_customer(data, model=get_model())
    return jsonify(res)

if __name__ == "__main__":
    print("[*] Starting web dashboard on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=False)
