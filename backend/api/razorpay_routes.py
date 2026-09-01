import os
import hmac
import hashlib
import json
from uuid import uuid4

import requests
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/razorpay", tags=["Razorpay"])


RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET")


class CreateOrderRequest(BaseModel):
    amount: float


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


@router.post("/create-order")
def create_razorpay_order(data: CreateOrderRequest):

    if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Razorpay API keys are not configured."
        )

    if data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than zero."
        )

    amount_in_paise = int(data.amount * 100)

    receipt = f"recoverai_{uuid4().hex[:12]}"

    payload = {
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": receipt,
        "notes": {
            "source": "RecoverAI",
            "purpose": "Revenue Recovery Demo"
        }
    }

    try:

        response = requests.post(
            "https://api.razorpay.com/v1/orders",
            auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET),
            json=payload,
            timeout=15
        )

        if not response.ok:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        order = response.json()

        return {
            "success": True,
            "key_id": RAZORPAY_KEY_ID,
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "receipt": order["receipt"]
        }

    except requests.RequestException as error:

        raise HTTPException(
            status_code=500,
            detail=f"Razorpay connection failed: {str(error)}"
        )


@router.post("/verify-payment")
def verify_payment(data: VerifyPaymentRequest):

    if not RAZORPAY_KEY_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Razorpay secret is not configured."
        )

    message = (
        f"{data.razorpay_order_id}|"
        f"{data.razorpay_payment_id}"
    )

    generated_signature = hmac.new(
        RAZORPAY_KEY_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(
        generated_signature,
        data.razorpay_signature
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid Razorpay payment signature."
        )

    return {
        "success": True,
        "message": "Payment verified successfully.",
        "razorpay_order_id": data.razorpay_order_id,
        "razorpay_payment_id": data.razorpay_payment_id
    }


@router.post("/webhook")
async def razorpay_webhook(request: Request):

    raw_body = await request.body()

    signature = request.headers.get(
        "X-Razorpay-Signature"
    )

    if not signature:
        raise HTTPException(
            status_code=400,
            detail="Missing Razorpay webhook signature."
        )

    if not RAZORPAY_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Webhook secret is not configured."
        )

    expected_signature = hmac.new(
        RAZORPAY_WEBHOOK_SECRET.encode(),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(
        expected_signature,
        signature
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid webhook signature."
        )

    try:
        event = json.loads(raw_body)

        event_name = event.get("event")

        payment = (
            event
            .get("payload", {})
            .get("payment", {})
            .get("entity", {})
        )

        payment_id = payment.get("id")
        order_id = payment.get("order_id")
        amount = payment.get("amount", 0)
        method = payment.get("method")

        print("================================")
        print("RAZORPAY WEBHOOK")
        print("EVENT:", event_name)
        print("PAYMENT:", payment_id)
        print("ORDER:", order_id)
        print("AMOUNT:", amount)
        print("METHOD:", method)
        print("================================")

        if event_name == "payment.failed":

            print("Payment failed → RecoverAI can analyze this transaction.")

        elif event_name == "payment.captured":

            print("Payment captured → Revenue successfully recovered.")

        elif event_name == "order.paid":

            print("Order paid → Recovery successful.")

        return {
            "success": True,
            "event": event_name
        }

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=400,
            detail="Invalid webhook payload."
        )