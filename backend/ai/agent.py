import joblib
import pandas as pd

from services.recovery_decision import decide_recovery_action
from ai.failure_intelligence import analyze_failure
from ai.recovery_priority import calculate_recovery_priority


# --------------------------------------------------
# Load trained ML model
# --------------------------------------------------

model = joblib.load("ai/recovery_model.joblib")


def analyze_transaction(transaction):
    """
    Analyze a transaction and generate
    a recovery recommendation.
    """

    # Convert transaction into DataFrame
    data = pd.DataFrame([transaction])

    # Get recovery probability
    probability = model.predict_proba(data)[0][1]

    recovery_probability = probability * 100

    failure_analysis = analyze_failure(
    transaction["failure_reason"],
    transaction["attempt_count"],
    transaction["checkout_abandoned"]
    )

    expected_recoverable_revenue = round(
    transaction["amount"] * recovery_probability / 100,
    2
    )

    recovery_priority = calculate_recovery_priority(
    transaction["amount"],
    recovery_probability,
    transaction["attempt_count"]
    )

    # Determine recovery potential
    if recovery_probability >= 70:
        recovery_potential = "HIGH"

    elif recovery_probability >= 40:
        recovery_potential = "MEDIUM"

    else:
        recovery_potential = "LOW"

    # Ask decision engine for action
    decision = decide_recovery_action(
    recovery_probability,
    transaction["amount"],
    transaction["failure_reason"],
    transaction["attempt_count"],
    transaction["checkout_abandoned"]
)

    return {
        "recovery_probability": round(
            recovery_probability,
            2
        ),
        "recovery_potential": recovery_potential,
        "expected_recoverable_revenue":expected_recoverable_revenue,
        "recovery_priority": recovery_priority["priority"],
        "priority_score": recovery_priority["priority_score"],
        "priority_reason": recovery_priority["priority_reason"],
        "recommended_action": decision["recommended_action"],
        "reason": decision["reason"],
        "priority": decision["priority"],
        "failure_category": failure_analysis["failure_category"],
        "recovery_strategy": failure_analysis["recovery_strategy"],
        "strategy_reason": failure_analysis["strategy_reason"],
        "urgency": failure_analysis["urgency"]
    }


# --------------------------------------------------
# Test transaction
# --------------------------------------------------

if __name__ == "__main__":

    transaction = {
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

    result = analyze_transaction(transaction)

    print("=" * 60)
    print("RecoverAI Intelligent Recovery Agent")
    print("=" * 60)

    print(
        f"Recovery Probability: "
        f"{result['recovery_probability']}%"
    )

    print(
        f"Recovery Potential: "
        f"{result['recovery_potential']}"
    )

    print(
        f"Recommended Action: "
        f"{result['recommended_action']}"
    )

    print(
        f"Priority: "
        f"{result['priority']}"
    )

    print(
        f"Reason: "
        f"{result['reason']}"
    )

    print("=" * 60)