def analyze_failure(
    failure_reason,
    attempt_count=1,
    checkout_abandoned=0
):
    """
    Analyze why a payment failed and recommend
    an appropriate recovery strategy.
    """

    failure_reason = (failure_reason or "").lower().strip()

    # Network-related failure
    if failure_reason in ["network_error", "timeout", "connection_error"]:
        return {
            "failure_category": "TECHNICAL",
            "recovery_strategy": "intelligent_retry",
            "strategy_reason": "The payment may have failed because of a temporary network issue.",
            "urgency": "MEDIUM"
        }

    # Insufficient balance
    if failure_reason in [
        "insufficient_funds",
        "insufficient_balance",
        "low_balance"
    ]:
        return {
            "failure_category": "CUSTOMER_FUNDS",
            "recovery_strategy": "send_payment_reminder",
            "strategy_reason": "The customer may not have sufficient funds. Repeated automatic retries should be avoided.",
            "urgency": "MEDIUM"
        }

    # Bank decline
    if failure_reason in [
        "bank_declined",
        "declined",
        "issuer_declined"
    ]:
        return {
            "failure_category": "BANK_DECLINE",
            "recovery_strategy": "suggest_alternate_payment",
            "strategy_reason": "The bank declined the transaction. Suggesting another payment method may improve recovery.",
            "urgency": "HIGH"
        }

    # Checkout abandonment
    if checkout_abandoned == 1:
        return {
            "failure_category": "CHECKOUT_ABANDONED",
            "recovery_strategy": "send_checkout_reminder",
            "strategy_reason": "The customer started checkout but did not complete the payment.",
            "urgency": "MEDIUM"
        }

    # Repeated failures
    if attempt_count >= 3:
        return {
            "failure_category": "REPEATED_FAILURE",
            "recovery_strategy": "escalate_recovery",
            "strategy_reason": "Multiple payment attempts have already failed. Further automatic retries may create unnecessary friction.",
            "urgency": "HIGH"
        }

    # Unknown failure
    return {
        "failure_category": "UNKNOWN",
        "recovery_strategy": "manual_review",
        "strategy_reason": "The failure reason could not be confidently classified.",
        "urgency": "LOW"
    }