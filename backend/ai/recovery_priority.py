def calculate_recovery_priority(
    amount,
    recovery_probability,
    attempt_count=1
):
    """
    Calculate the business priority of a failed transaction.
    """

    amount = float(amount)
    probability = float(recovery_probability)
    attempt_count = int(attempt_count)

    # Avoid wasting effort on transactions that have
    # already failed repeatedly.
    if attempt_count >= 3:
        return {
            "priority": "LOW",
            "priority_score": 25,
            "priority_reason": (
                "Multiple attempts have already failed. "
                "Further automated recovery may create unnecessary friction."
            )
        }

    # High-value + high recovery probability
    if amount >= 10000 and probability >= 60:
        return {
            "priority": "CRITICAL",
            "priority_score": 95,
            "priority_reason": (
                "High-value transaction with strong recovery potential. "
                "This case should receive immediate attention."
            )
        }

    # High-value transaction
    if amount >= 10000:
        return {
            "priority": "HIGH",
            "priority_score": 80,
            "priority_reason": (
                "The transaction represents significant potential revenue."
            )
        }

    # Strong recovery probability
    if probability >= 70:
        return {
            "priority": "HIGH",
            "priority_score": 75,
            "priority_reason": (
                "The transaction has a strong probability of recovery."
            )
        }

    # Medium opportunity
    if probability >= 40:
        return {
            "priority": "MEDIUM",
            "priority_score": 55,
            "priority_reason": (
                "The transaction has a reasonable recovery opportunity."
            )
        }

    # Low opportunity
    return {
        "priority": "LOW",
        "priority_score": 30,
        "priority_reason": (
            "Recovery probability is relatively low, so this case "
            "should receive lower priority."
        )
    }