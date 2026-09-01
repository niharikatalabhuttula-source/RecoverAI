def decide_recovery_action(
    recovery_probability: float,
    amount: float,
    failure_reason: str,
    attempt_count: int,
    checkout_abandoned: int = 0
):
    """
    Decide the safest recovery strategy for a failed transaction.
    """

    probability = float(recovery_probability)
    amount = float(amount)
    attempt_count = int(attempt_count)

    reason = failure_reason.lower().replace("_", " ")

    # ---------------------------------------------------------
    # 1. Protect against repeated automated attempts
    # ---------------------------------------------------------

    if attempt_count >= 3:
        return {
            "recommended_action": "escalate_to_human",
            "priority": "HIGH",
            "reason": (
                "Multiple payment attempts have already failed. "
                "RecoverAI avoids repeated automated retries and "
                "recommends human review."
            )
        }

    # ---------------------------------------------------------
    # 2. Insufficient funds
    # ---------------------------------------------------------

    if "insufficient" in reason:
        return {
            "recommended_action": "send_payment_link",
            "priority": "MEDIUM",
            "reason": (
                "The payment appears to have failed because of "
                "insufficient funds. RecoverAI recommends giving "
                "the customer another opportunity to complete payment "
                "instead of immediately retrying."
            )
        }

    # ---------------------------------------------------------
    # 3. Temporary technical/network failures
    # ---------------------------------------------------------

    if (
        "network" in reason
        or "timeout" in reason
        or "technical" in reason
    ):
        if probability >= 70:
            return {
                "recommended_action": "retry_payment",
                "priority": "HIGH",
                "reason": (
                    "The failure appears temporary and the recovery "
                    "probability is high. RecoverAI recommends a "
                    "controlled payment retry."
                )
            }

        elif probability >= 40:
            return {
                "recommended_action": "wait_and_retry",
                "priority": "MEDIUM",
                "reason": (
                    "The failure may be temporary, but recovery "
                    "confidence is moderate. RecoverAI recommends "
                    "waiting before attempting another payment."
                )
            }

        else:
            return {
                "recommended_action": "send_payment_link",
                "priority": "LOW",
                "reason": (
                    "Recovery probability is low. RecoverAI avoids "
                    "repeated automated retries and provides an "
                    "alternative payment path."
                )
            }

    # ---------------------------------------------------------
    # 4. Abandoned checkout
    # ---------------------------------------------------------

    if checkout_abandoned == 1:
        return {
            "recommended_action": "send_payment_reminder",
            "priority": "MEDIUM",
            "reason": (
                "The customer abandoned checkout before completing "
                "payment. RecoverAI recommends a low-friction reminder."
            )
        }

    # ---------------------------------------------------------
    # 5. High-value transactions
    # ---------------------------------------------------------

    if amount >= 10000 and probability >= 60:
        return {
            "recommended_action": "send_payment_link",
            "priority": "HIGH",
            "reason": (
                "This is a high-value transaction with a strong "
                "recovery probability. RecoverAI prioritizes the case "
                "and recommends a direct payment link."
            )
        }

    # ---------------------------------------------------------
    # 6. General probability-based strategy
    # ---------------------------------------------------------

    if probability >= 70:
        return {
            "recommended_action": "retry_payment",
            "priority": "HIGH",
            "reason": (
                "The transaction has a high recovery probability. "
                "RecoverAI recommends an automated retry."
            )
        }

    elif probability >= 40:
        return {
            "recommended_action": "send_payment_reminder",
            "priority": "MEDIUM",
            "reason": (
                "The transaction has a moderate recovery probability. "
                "RecoverAI recommends a low-friction reminder."
            )
        }

    # ---------------------------------------------------------
    # 7. Low probability
    # ---------------------------------------------------------

    return {
        "recommended_action": "escalate_to_human",
        "priority": "LOW",
        "reason": (
            "The recovery probability is low. RecoverAI avoids "
            "aggressive automated actions and recommends a safer "
            "recovery path."
        )
    }