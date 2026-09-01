import pandas as pd


# Load dataset
df = pd.read_csv("data/transactions.csv")


print("=" * 60)
print("RecoverAI Dataset Inspection")
print("=" * 60)

# 1. Dataset size
print("\n1. Dataset Shape")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")


# 2. Column names
print("\n2. Columns")
for column in df.columns:
    print("-", column)


# 3. Missing values
print("\n3. Missing Values")
print(df.isnull().sum())


# 4. Duplicate transactions
print("\n4. Duplicate Transaction IDs")
print(df["transaction_id"].duplicated().sum())


# 5. Payment status
print("\n5. Payment Status Distribution")
print(df["payment_status"].value_counts())


# 6. Recovery action
print("\n6. Recovery Action Distribution")
print(df["recovery_action"].value_counts())


# 7. Recovery success
print("\n7. Recovery Success Distribution")
print(df["recovery_success"].value_counts())


# 8. Numerical statistics
print("\n8. Numerical Statistics")
print(df[
    [
        "amount",
        "attempt_count",
        "previous_success_rate",
        "days_overdue",
        "recovery_attempts",
        "recovered_amount"
    ]
].describe())


# 9. Total revenue
print("\n9. Revenue Summary")

total_amount = df["amount"].sum()
recovered_amount = df["recovered_amount"].sum()

print(f"Total transaction value: ₹{total_amount:,.2f}")
print(f"Recovered revenue: ₹{recovered_amount:,.2f}")


# 10. Recovery rate
recovery_rate = df["recovery_success"].mean() * 100

print(f"Overall recovery success rate: {recovery_rate:.2f}%")

print("\n" + "=" * 60)
print("Dataset inspection completed.")
print("=" * 60)