from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from razorpay_routes import router as razorpay_router

from ai.agent import analyze_transaction
from ai.recovery_queue import build_recovery_queue


app = FastAPI(
    title="RecoverAI API",
    description="Intelligent Revenue Recovery Agent",
    version="1.0.0"
)
app.include_router(razorpay_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Transaction(BaseModel):
    amount: float
    payment_method: str
    payment_status: str
    failure_reason: str
    attempt_count: int
    checkout_abandoned: int
    checkout_duration_seconds: int
    previous_transactions: int
    previous_successful_transactions: int
    previous_success_rate: float
    is_subscription: int
    days_overdue: int


@app.get("/")
def home():
    return {
        "message": "RecoverAI API is running",
        "status": "active"
    }


@app.post("/analyze")
def analyze(transaction: Transaction):

    result = analyze_transaction(
        transaction.model_dump()
    )

    return {
        "success": True,
        "transaction": transaction.model_dump(),
        "analysis": result
    }
class RecoveryQueueRequest(BaseModel):
    transactions: list[dict]

@app.post("/recovery-queue")
def recovery_queue(request: RecoveryQueueRequest):
    """
    Rank failed transactions by recovery opportunity.
    """

    queue = build_recovery_queue(request.transactions)

    return {
        "success": True,
        "total_transactions": len(queue),
        "recovery_queue": queue
    }

