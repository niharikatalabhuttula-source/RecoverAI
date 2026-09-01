import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv("data/transactions.csv")


# --------------------------------------------------
# 2. Keep only transactions that need recovery
# --------------------------------------------------

df = df[df["payment_status"].isin(["failed", "abandoned"])].copy()


# --------------------------------------------------
# 3. Features
# --------------------------------------------------

features = [
    "amount",
    "payment_method",
    "payment_status",
    "failure_reason",
    "attempt_count",
    "checkout_abandoned",
    "checkout_duration_seconds",
    "previous_transactions",
    "previous_successful_transactions",
    "previous_success_rate",
    "is_subscription",
    "days_overdue"
]

target = "recovery_success"


X = df[features]
y = df[target]


# --------------------------------------------------
# 4. Identify categorical and numerical features
# --------------------------------------------------

categorical_features = [
    "payment_method",
    "payment_status",
    "failure_reason"
]

numerical_features = [
    "amount",
    "attempt_count",
    "checkout_abandoned",
    "checkout_duration_seconds",
    "previous_transactions",
    "previous_successful_transactions",
    "previous_success_rate",
    "is_subscription",
    "days_overdue"
]


# --------------------------------------------------
# 5. Preprocessing
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# --------------------------------------------------
# 6. Machine Learning model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# --------------------------------------------------
# 7. Create ML pipeline
# --------------------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# --------------------------------------------------
# 8. Split data
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# 9. Train
# --------------------------------------------------

print("=" * 60)
print("Training RecoverAI Recovery Prediction Model")
print("=" * 60)

pipeline.fit(X_train, y_train)


# --------------------------------------------------
# 10. Evaluate
# --------------------------------------------------

predictions = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:")
print(f"{accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# --------------------------------------------------
# 11. Save model
# --------------------------------------------------

model_path = "ai/recovery_model.joblib"

joblib.dump(pipeline, model_path)

print("\nModel saved successfully:")
print(model_path)

print("\nTraining completed.")