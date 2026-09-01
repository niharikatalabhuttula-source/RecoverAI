import joblib
import pandas as pd


# Load trained model
model = joblib.load("ai/recovery_model.joblib")


# Example transaction
transaction = pd.DataFrame([
    {
        "amount": 4500,
        "payment_method": "UPI",
        "payment_status": "failed",
        "failure_reason": "network_error",
        "attempt_count": 1,
        "checkout_abandoned": 0,
        "checkout_duration_seconds": 180,
        "previous_transactions": 10,
        "previous_successful_transactions": 9,
        "previous_success_rate": 0.90,
        "is_subscription": 0,
        "days_overdue": 0
    }
])


# Predict probability
probability = model.predict_proba(transaction)[0][1]

# Convert to percentage
recovery_probability = probability * 100


# Determine recovery potential
if recovery_probability >= 70:
    recovery_potential = "HIGH"
elif recovery_probability >= 40:
    recovery_potential = "MEDIUM"
else:
    recovery_potential = "LOW"


print("=" * 50)
print("RecoverAI Recovery Prediction")
print("=" * 50)

print(f"Recovery Probability: {recovery_probability:.2f}%")
print(f"Recovery Potential: {recovery_potential}")

print("=" * 50)