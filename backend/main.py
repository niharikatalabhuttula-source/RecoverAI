from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import razorpay
import os
from dotenv import load_dotenv
from datetime import datetime


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")


# ============================================================
# RAZORPAY CLIENT
# ============================================================

if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(
        auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
    )
else:
    razorpay_client = None


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="RecoverAI API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATA MODELS
# ============================================================

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    recovery_probability: float


class RecoveryQueueRequest(BaseModel):
    transactions: List[Transaction]


class AnalyzeRequest(BaseModel):
    amount: float
    payment_method: str
    payment_status: str = "failed"
    failure_reason: str
    attempt_count: int = 1
    checkout_abandoned: int = 0
    checkout_duration_seconds: int = 180
    previous_transactions: int = 10
    previous_successful_transactions: int = 9
    previous_success_rate: float = 0.9
    is_subscription: int = 0
    days_overdue: int = 0


class CreateOrderRequest(BaseModel):
    amount: float


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class ExecuteRecoveryRequest(BaseModel):
    transaction_id: str
    action: str


# ============================================================
# SAMPLE TRANSACTION DATA
# ============================================================

TRANSACTIONS = [
    {
        "transaction_id": "TXN-92831",
        "amount": 4500,
        "payment_method": "UPI",
        "failure_reason": "network_error",
        "recovery_probability": 65.5,
        "status": "Medium",
        "recommended_action": "payment_reminder"
    },
    {
        "transaction_id": "TXN-92830",
        "amount": 12800,
        "payment_method": "CARD",
        "failure_reason": "technical_error",
        "recovery_probability": 84.2,
        "status": "High",
        "recommended_action": "retry_payment"
    },
    {
        "transaction_id": "TXN-92829",
        "amount": 2100,
        "payment_method": "NETBANKING",
        "failure_reason": "insufficient_funds",
        "recovery_probability": 31.8,
        "status": "Low",
        "recommended_action": "human_escalation"
    },
    {
        "transaction_id": "TXN-92828",
        "amount": 7650,
        "payment_method": "UPI",
        "failure_reason": "timeout",
        "recovery_probability": 76.4,
        "status": "High",
        "recommended_action": "retry_payment"
    }
]


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "RecoverAI Backend is running",
        "razorpay_configured": razorpay_client is not None,
        "version": "1.0.0"
    }


# ============================================================
# RAZORPAY CONFIG
# ============================================================

@app.get("/razorpay-config")
def razorpay_config():

    if not RAZORPAY_KEY_ID:

        raise HTTPException(
            status_code=500,
            detail="Razorpay Key ID is not configured"
        )

    return {
        "key_id": RAZORPAY_KEY_ID
    }


# ============================================================
# CREATE RAZORPAY ORDER
# ============================================================

@app.post("/create-order")
def create_order(request: CreateOrderRequest):

    if razorpay_client is None:

        raise HTTPException(
            status_code=500,
            detail=(
                "Razorpay credentials are missing. "
                "Check RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in .env"
            )
        )

    if request.amount <= 0:

        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero"
        )

    try:

        amount_in_paise = int(
            round(request.amount * 100)
        )

        receipt = (
            f"recoverai_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )

        order_data = {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": receipt
        }

        order = razorpay_client.order.create(
            data=order_data
        )

        return {
            "success": True,
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key_id": RAZORPAY_KEY_ID
        }

    except Exception as e:

        print(
            "RAZORPAY ORDER ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"Razorpay order creation failed: {str(e)}"
        )


# ============================================================
# VERIFY RAZORPAY PAYMENT
# ============================================================

@app.post("/verify-payment")
def verify_payment(request: VerifyPaymentRequest):

    if razorpay_client is None:

        raise HTTPException(
            status_code=500,
            detail="Razorpay credentials are not configured"
        )

    try:

        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id":
                request.razorpay_order_id,

            "razorpay_payment_id":
                request.razorpay_payment_id,

            "razorpay_signature":
                request.razorpay_signature
        })

        return {
            "success": True,
            "message": "Payment verified successfully",
            "payment_id":
                request.razorpay_payment_id,
            "order_id":
                request.razorpay_order_id
        }

    except Exception as e:

        print(
            "PAYMENT VERIFICATION ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=400,
            detail="Payment verification failed"
        )


# ============================================================
# ANALYZE TRANSACTION
# ============================================================

@app.post("/analyze")
def analyze_transaction(
    transaction: AnalyzeRequest
):

    amount = transaction.amount
    method = transaction.payment_method
    reason = transaction.failure_reason

    # --------------------------------------------------------
    # GENERATE TRANSACTION ID
    # --------------------------------------------------------

    transaction_id = (
        f"TXN-{datetime.now().strftime('%H%M%S%f')[:8]}"
    )

    # --------------------------------------------------------
    # Recovery probability
    # --------------------------------------------------------

    probability = 50.0

    if method == "UPI":

        probability += 5

    elif method == "CARD":

        probability += 8

    elif method == "NETBANKING":

        probability += 2

    elif method == "WALLET":

        probability += 4

    # --------------------------------------------------------
    # Failure reason
    # --------------------------------------------------------

    if reason == "network_error":

        probability += 8

    elif reason == "timeout":

        probability += 6

    elif reason == "technical_error":

        probability += 5

    elif reason == "bank_error":

        probability += 2

    elif reason == "insufficient_funds":

        probability -= 15

    # --------------------------------------------------------
    # Customer history
    # --------------------------------------------------------

    if transaction.previous_success_rate >= 0.8:

        probability += 10

    elif transaction.previous_success_rate >= 0.5:

        probability += 5

    else:

        probability -= 5

    # --------------------------------------------------------
    # Attempts
    # --------------------------------------------------------

    if transaction.attempt_count > 2:

        probability -= 8

    # --------------------------------------------------------
    # Abandoned checkout
    # --------------------------------------------------------

    if transaction.checkout_abandoned == 1:

        probability -= 5

    probability = max(
        5,
        min(95, probability)
    )

    probability = round(
        probability,
        1
    )

    # --------------------------------------------------------
    # Expected recovery
    # --------------------------------------------------------

    expected_revenue = round(
        amount * probability / 100,
        2
    )

    revenue_at_risk = round(
        amount,
        2
    )

    # --------------------------------------------------------
    # Priority score
    # --------------------------------------------------------

    priority_score = (
        probability * 0.65
        + min(amount / 1000, 100) * 0.35
    )

    priority_score = round(
        min(priority_score, 100),
        1
    )

    if priority_score >= 75:

        recovery_priority = "Critical"

    elif priority_score >= 55:

        recovery_priority = "High"

    elif priority_score >= 35:

        recovery_priority = "Medium"

    else:

        recovery_priority = "Low"

    # --------------------------------------------------------
    # Recovery action
    # --------------------------------------------------------

    if probability >= 75:

        recommended_action = "retry_payment"

        recovery_strategy = "automated_retry"

        urgency = "High"

        reason_text = (
            "The transaction has a strong recovery probability "
            "and can be safely retried automatically."
        )

    elif probability >= 50:

        recommended_action = "payment_reminder"

        recovery_strategy = "customer_reminder"

        urgency = "Medium"

        reason_text = (
            "The transaction has a moderate recovery probability. "
            "A low-friction payment reminder is recommended before "
            "attempting further recovery."
        )

    else:

        recommended_action = "human_escalation"

        recovery_strategy = "manual_review"

        urgency = "Low"

        reason_text = (
            "The transaction has a lower recovery probability. "
            "RecoverAI avoids aggressive retries and recommends "
            "manual intervention."
        )

    # --------------------------------------------------------
    # Failure category
    # --------------------------------------------------------

    if reason in [
        "network_error",
        "timeout",
        "technical_error"
    ]:

        failure_category = "technical_failure"

    elif reason == "bank_error":

        failure_category = "bank_failure"

    elif reason == "insufficient_funds":

        failure_category = "financial_failure"

    else:

        failure_category = "payment_failure"

    # --------------------------------------------------------
    # Failure severity
    # --------------------------------------------------------

    if reason in [
        "technical_error",
        "bank_error"
    ]:

        failure_severity = "Medium"

    elif reason == "insufficient_funds":

        failure_severity = "High"

    elif reason in [
        "network_error",
        "timeout"
    ]:

        failure_severity = "Low"

    else:

        failure_severity = "Medium"

    # --------------------------------------------------------
    # Retry safety
    # --------------------------------------------------------

    if reason in [
        "network_error",
        "timeout",
        "technical_error"
    ]:

        retry_safety = "Safe"

    elif reason == "insufficient_funds":

        retry_safety = "Unsafe"

    elif reason == "bank_error":

        retry_safety = "Moderate"

    else:

        retry_safety = "Moderate"

    # --------------------------------------------------------
    # Customer quality
    # --------------------------------------------------------

    if transaction.previous_success_rate >= 0.8:

        customer_quality = "High-value / Reliable"

    elif transaction.previous_success_rate >= 0.5:

        customer_quality = "Moderate"

    else:

        customer_quality = "Low confidence"

    # --------------------------------------------------------
    # Explanations
    # --------------------------------------------------------

    priority_reason = (
        f"Recovery probability is {probability}% and the "
        f"transaction value is ₹{amount:,.0f}. "
        f"RecoverAI balances revenue value with recovery likelihood."
    )

    strategy_reason = (
        f"The payment failed because of "
        f"{reason.replace('_', ' ')}. "
        f"Based on the payment method, customer history and "
        f"failure pattern, RecoverAI selected "
        f"{recommended_action.replace('_', ' ')} "
        f"as the safest recovery strategy."
    )

    # --------------------------------------------------------
    # SAVE NEW TRANSACTION
    # --------------------------------------------------------

    new_transaction = {

        "transaction_id":
            transaction_id,

        "amount":
            amount,

        "payment_method":
            method,

        "failure_reason":
            reason,

        "recovery_probability":
            probability,

        "status":
            recovery_priority,

        "recommended_action":
            recommended_action,

        "expected_recoverable_revenue":
            expected_revenue,

        "executed":
            False
    }

    TRANSACTIONS.insert(
        0,
        new_transaction
    )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {

        "success": True,

        "transaction_id":
            transaction_id,

        "analysis": {

            "recovery_probability":
                probability,

            "recovery_potential":
                f"₹{expected_revenue:,.2f}",

            "expected_recoverable_revenue":
                expected_revenue,

            "revenue_at_risk":
                revenue_at_risk,

            "priority":
                recovery_priority,

            "recovery_priority":
                recovery_priority,

            "priority_score":
                priority_score,

            "priority_reason":
                priority_reason,

            "recommended_action":
                recommended_action,

            "reason":
                reason_text,

            "failure_category":
                failure_category,

            "failure_severity":
                failure_severity,

            "retry_safety":
                retry_safety,

            "customer_quality":
                customer_quality,

            "recovery_strategy":
                recovery_strategy,

            "urgency":
                urgency,

            "strategy_reason":
                strategy_reason
        }
    }


# ============================================================
# RECOVERY QUEUE - GET
# ============================================================

@app.get("/recovery-queue")
def get_recovery_queue():

    queue = []

    for transaction in TRANSACTIONS:

        expected_revenue = round(
            transaction["amount"]
            * transaction["recovery_probability"]
            / 100,
            2
        )

        queue.append({

            "transaction_id":
                transaction["transaction_id"],

            "amount":
                transaction["amount"],

            "payment_method":
                transaction["payment_method"],

            "recovery_probability":
                transaction["recovery_probability"],

            "expected_recoverable_revenue":
                expected_revenue,

            "recommended_action":
                transaction["recommended_action"]
        })

    queue.sort(
        key=lambda x: (
            x["recovery_probability"],
            x["expected_recoverable_revenue"]
        ),
        reverse=True
    )

    for index, item in enumerate(
        queue,
        start=1
    ):

        item["rank"] = index

    return {

        "recovery_queue":
            queue,

        "total_cases":
            len(queue)
    }


# ============================================================
# RECOVERY QUEUE - POST
# ============================================================

@app.post("/recovery-queue")
def recovery_queue(
    request: RecoveryQueueRequest
):

    queue = []

    for transaction in request.transactions:

        expected_revenue = round(
            transaction.amount
            * transaction.recovery_probability
            / 100,
            2
        )

        queue.append({

            "transaction_id":
                transaction.transaction_id,

            "amount":
                transaction.amount,

            "recovery_probability":
                transaction.recovery_probability,

            "expected_recoverable_revenue":
                expected_revenue
        })

    queue.sort(
        key=lambda x: (
            x["recovery_probability"],
            x["expected_recoverable_revenue"]
        ),
        reverse=True
    )

    for index, item in enumerate(
        queue,
        start=1
    ):

        item["rank"] = index

    return {

        "recovery_queue":
            queue,

        "total_cases":
            len(queue)
    }


# ============================================================
# EXECUTE RECOVERY ACTION
# ============================================================

@app.post("/execute-recovery")
def execute_recovery(
    request: ExecuteRecoveryRequest
):

    transaction = None

    for item in TRANSACTIONS:

        if (
            item["transaction_id"]
            == request.transaction_id
        ):

            transaction = item
            break

    if transaction is None:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    transaction["executed"] = True

    transaction["executed_action"] = (
        request.action
    )

    transaction["status"] = "Recovery Processed"

    return {

        "success": True,

        "message": (
            f"Recovery action "
            f"'{request.action.replace('_', ' ')}' "
            f"executed successfully for "
            f"{request.transaction_id}."
        ),

        "transaction_id":
            request.transaction_id,

        "action":
            request.action,

        "status":
            "Recovery Processed"
    }


# ============================================================
# GET TRANSACTIONS
# ============================================================

@app.get("/transactions")
def get_transactions():

    return {

        "transactions":
            TRANSACTIONS,

        "total":
            len(TRANSACTIONS)
    }


# ============================================================
# DASHBOARD METRICS
# ============================================================

@app.get("/dashboard-metrics")
def dashboard_metrics():

    total_transactions = len(
        TRANSACTIONS
    )

    if total_transactions == 0:

        return {

            "revenue_at_risk": 0,

            "expected_recoverable_revenue": 0,

            "recovery_rate": 0,

            "average_recovery_probability": 0,

            "active_cases": 0,

            "total_cases": 0,

            "high_priority_cases": 0,

            "ai_decisions": 0,

            "currency": "INR"
        }

    revenue_at_risk = sum(
        transaction["amount"]
        for transaction in TRANSACTIONS
    )

    expected_recovery = sum(
        transaction["amount"]
        * transaction["recovery_probability"]
        / 100
        for transaction in TRANSACTIONS
    )

    average_probability = (
        sum(
            transaction["recovery_probability"]
            for transaction in TRANSACTIONS
        )
        / total_transactions
    )

    high_priority_cases = sum(
        1
        for transaction in TRANSACTIONS
        if transaction["recovery_probability"] >= 70
    )

    recovery_rate = round(
        expected_recovery
        / revenue_at_risk
        * 100,
        1
    ) if revenue_at_risk > 0 else 0

    return {

        "revenue_at_risk":
            round(
                revenue_at_risk,
                2
            ),

        "expected_recoverable_revenue":
            round(
                expected_recovery,
                2
            ),

        "recovery_rate":
            recovery_rate,

        "average_recovery_probability":
            round(
                average_probability,
                1
            ),

        "active_cases":
            total_transactions,

        "total_cases":
            total_transactions,

        "high_priority_cases":
            high_priority_cases,

        "ai_decisions":
            total_transactions,

        "currency":
            "INR"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {

        "status":
            "healthy",

        "service":
            "RecoverAI",

        "razorpay_configured":
            razorpay_client is not None
    }