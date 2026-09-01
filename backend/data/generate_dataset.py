import random
import pandas as pd
import numpy as np


# Make results reproducible
random.seed(42)
np.random.seed(42)


NUM_TRANSACTIONS = 10000


def generate_transaction(transaction_number):
    transaction_id = f"TX{transaction_number:05d}"
    customer_id = f"C{random.randint(1, 2500):04d}"

    amount = round(random.uniform(200, 50000), 2)

    payment_method = random.choice([
        "UPI",
        "CARD",
        "NETBANKING",
        "WALLET"
    ])

    transaction_type = random.choices(
        ["success", "failed", "abandoned"],
        weights=[0.65, 0.25, 0.10]
    )[0]

    if transaction_type == "success":
        payment_status = "success"
        failure_reason = "none"
        checkout_abandoned = 0

    elif transaction_type == "failed":
        payment_status = "failed"
        failure_reason = random.choice([
            "network_error",
            "bank_error",
            "insufficient_funds",
            "technical_error",
            "timeout"
        ])
        checkout_abandoned = 0

    else:
        payment_status = "abandoned"
        failure_reason = "checkout_dropoff"
        checkout_abandoned = 1

    if payment_status == "success":
        attempt_count = 0
    else:
        attempt_count = random.randint(0, 4)

    checkout_duration_seconds = random.randint(10, 600)

    previous_transactions = random.randint(1, 20)

    previous_successful_transactions = random.randint(
        0,
        previous_transactions
    )

    previous_success_rate = round(
        previous_successful_transactions / previous_transactions,
        2
    )

    is_subscription = random.choice([0, 1])

    if is_subscription:
        days_overdue = random.choices(
            [0, 1, 3, 7, 15, 30],
            weights=[50, 15, 10, 10, 8, 7]
        )[0]
    else:
        days_overdue = 0

    recovery_attempts = 0

    recovery_action = "none"

    if payment_status == "failed":

        if failure_reason in ["network_error", "timeout"]:
            recovery_action = "retry_payment"

        elif failure_reason == "insufficient_funds":
            recovery_action = "send_reminder"

        elif failure_reason in ["bank_error", "technical_error"]:
            recovery_action = "payment_link"

    elif payment_status == "abandoned":

        recovery_action = random.choice([
            "payment_link",
            "send_reminder"
        ])

    # Determine whether recovery was successful.
    recovery_success = 0

    if payment_status == "success":

        recovery_success = 1

    elif recovery_action == "retry_payment":

        if attempt_count <= 1:
            recovery_success = random.choices(
                [1, 0],
                weights=[0.70, 0.30]
            )[0]

    elif recovery_action == "payment_link":

        if previous_success_rate >= 0.60:
            recovery_success = random.choices(
                [1, 0],
                weights=[0.65, 0.35]
            )[0]
        else:
            recovery_success = random.choices(
                [1, 0],
                weights=[0.35, 0.65]
            )[0]

    elif recovery_action == "send_reminder":

        if days_overdue <= 3:
            recovery_success = random.choices(
                [1, 0],
                weights=[0.50, 0.50]
            )[0]
        else:
            recovery_success = random.choices(
                [1, 0],
                weights=[0.25, 0.75]
            )[0]

    # Number of automated recovery attempts
    if payment_status != "success":
        recovery_attempts = random.randint(0, 2)

    recovered_amount = amount if recovery_success == 1 else 0

    return {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "amount": amount,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "failure_reason": failure_reason,
        "attempt_count": attempt_count,
        "checkout_abandoned": checkout_abandoned,
        "checkout_duration_seconds": checkout_duration_seconds,
        "previous_transactions": previous_transactions,
        "previous_successful_transactions": previous_successful_transactions,
        "previous_success_rate": previous_success_rate,
        "is_subscription": is_subscription,
        "days_overdue": days_overdue,
        "recovery_attempts": recovery_attempts,
        "recovery_action": recovery_action,
        "recovery_success": recovery_success,
        "recovered_amount": recovered_amount
    }


def main():
    transactions = []

    for i in range(1, NUM_TRANSACTIONS + 1):
        transactions.append(generate_transaction(i))

    df = pd.DataFrame(transactions)

    output_file = "transactions.csv"

    df.to_csv(output_file, index=False)

    print("=" * 50)
    print("RecoverAI Synthetic Dataset Generated")
    print("=" * 50)
    print(f"Transactions: {len(df):,}")
    print(f"Total transaction value: ₹{df['amount'].sum():,.2f}")
    print(
        f"Revenue recovered: "
        f"₹{df['recovered_amount'].sum():,.2f}"
    )
    print()
    print("Payment status distribution:")
    print(df["payment_status"].value_counts())
    print()
    print("Recovery action distribution:")
    print(df["recovery_action"].value_counts())
    print()
    print("Dataset saved as:")
    print(output_file)


if __name__ == "__main__":
    main()