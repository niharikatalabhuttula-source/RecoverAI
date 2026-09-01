def build_recovery_queue(transactions):
    """
    Rank failed transactions based on their
    recovery priority and expected recoverable revenue.
    """

    queue = []

    for transaction in transactions:

        amount = float(transaction.get("amount", 0))
        probability = float(
            transaction.get("recovery_probability", 0)
        )

        expected_revenue = round(
            amount * probability / 100,
            2
        )

        # Business opportunity score
        opportunity_score = round(
            expected_revenue * 0.7
            + probability * 0.3,
            2
        )

        queue.append({
            "transaction_id": transaction.get(
                "transaction_id",
                "unknown"
            ),
            "amount": amount,
            "recovery_probability": probability,
            "expected_recoverable_revenue": expected_revenue,
            "opportunity_score": opportunity_score
        })

    # Highest opportunity first
    queue.sort(
        key=lambda x: x["opportunity_score"],
        reverse=True
    )

    # Add ranking
    for index, item in enumerate(queue, start=1):
        item["rank"] = index

    return queue