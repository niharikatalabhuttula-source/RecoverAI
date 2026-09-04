
# RecoverAI

## AI-Powered Revenue Recovery System

RecoverAI is an AI-powered revenue recovery platform designed to help businesses recover revenue from failed payments.

The system analyzes failed transactions, estimates their recovery probability, identifies the safest recovery strategy, prioritizes recovery opportunities, and provides an interactive dashboard for monitoring revenue at risk and expected recovery.

RecoverAI also integrates with Razorpay Test Mode to demonstrate a complete payment and recovery workflow.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Key Features](#key-features)
- [How RecoverAI Works](#how-recoverai-works)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Backend](#backend)
- [Frontend](#frontend)
- [Razorpay Integration](#razorpay-integration)
- [Installation and Setup](#installation-and-setup)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Testing the Application](#testing-the-application)
- [Screenshots](#screenshots)
- [Security](#security)
- [Future Enhancements](#future-enhancements)
- [Use Cases](#use-cases)
- [Project Status](#project-status)
- [Team](#team)
- [License](#license)

---

# Overview

Failed payments are a major source of revenue leakage for digital businesses.

A payment may fail because of:

- Network errors
- Bank errors
- Technical failures
- Timeouts
- Insufficient funds
- Other payment-related issues

Not every failed transaction should be handled in the same way.

Retrying every failed payment can create unnecessary retries, while ignoring potentially recoverable transactions can result in lost revenue.

RecoverAI addresses this problem by analyzing each failed transaction and recommending an appropriate recovery action.

---

# Problem Statement

Businesses lose significant revenue when legitimate payment attempts fail.

Traditional recovery systems often rely on fixed rules such as:

- Retry every failed payment
- Send the same reminder to every customer
- Manually review failed transactions
- Treat all failures equally

These approaches do not consider:

- Payment method
- Failure reason
- Customer payment history
- Previous success rate
- Number of attempts
- Transaction value
- Recovery probability

RecoverAI provides an intelligent decision layer that evaluates these factors and recommends a suitable recovery strategy.

---

# Solution

RecoverAI provides an end-to-end revenue recovery workflow.

The platform:

1. Accepts failed transaction information.
2. Analyzes the transaction.
3. Calculates recovery probability.
4. Estimates expected recoverable revenue.
5. Calculates a priority score.
6. Classifies recovery priority.
7. Identifies the failure category and severity.
8. Evaluates retry safety.
9. Determines customer quality.
10. Recommends a recovery action.
11. Adds transactions to the recovery workflow.
12. Displays recovery opportunities through a dashboard.
13. Provides Razorpay Test Mode payment integration.
14. Verifies successful Razorpay payments.

---

# Key Features

## 1. Transaction Analysis

RecoverAI analyzes failed payment transactions using factors such as:

- Transaction amount
- Payment method
- Failure reason
- Attempt count
- Customer payment history
- Previous success rate
- Checkout abandonment
- Subscription status
- Days overdue

---

## 2. Recovery Probability

The system calculates a recovery probability for every analyzed transaction.

Example:

```text
Recovery Probability: 84.2%

This helps identify transactions that are more likely to be successfully recovered.


---

3. Expected Recoverable Revenue

RecoverAI estimates how much revenue could potentially be recovered.

The calculation is based on:

Expected Recovery =
Transaction Amount × Recovery Probability / 100


---

4. Recovery Priority

Transactions are prioritized using a priority score that considers:

Recovery probability

Transaction value


Transactions can be classified as:

Critical
High
Medium
Low


---

5. AI Decision Intelligence

RecoverAI provides additional transaction intelligence including:

Failure Category

Failure Severity

Retry Safety

Customer Quality

Recovery Strategy

Urgency

Priority Score

AI Reasoning



---

6. Recommended Recovery Action

Based on the transaction analysis, RecoverAI recommends one of the following actions:

Retry Payment

Used when the transaction has a high recovery probability and retrying is considered safe.

Payment Reminder

Used when the transaction has moderate recovery potential and a customer reminder is more appropriate.

Human Escalation

Used when the recovery probability is lower or aggressive automated retries are not recommended.


---

7. Recovery Queue

The Recovery Queue displays high-priority recovery opportunities.

Each queue item contains:

Rank

Transaction ID

Transaction amount

Payment method

Recovery probability

Expected recoverable revenue


Transactions are ordered based on recovery opportunity.


---

8. Dashboard Metrics

The dashboard displays:

Revenue at Risk

Expected Recovery

Active Cases

Average Recovery Probability

Recovery Rate

High Priority Cases

AI Decisions



---

9. Recent Transactions

RecoverAI displays recently analyzed transactions along with:

Transaction ID

Payment method

Amount

Recovery probability

Recovery priority

Recommended recovery action



---

10. Recovery Activity

The dashboard provides a recovery activity section to show recent system actions and recovery workflow events.


---

11. Razorpay Test Mode Integration

RecoverAI integrates with Razorpay Test Mode to demonstrate a payment recovery workflow.

The system supports:

Razorpay order creation

Test payment checkout

Payment success handling

Payment failure handling

Payment signature verification


No real money is required for the demonstration.


---

How RecoverAI Works

The overall workflow is:

Failed Payment
       |
       v
Transaction Data
       |
       v
RecoverAI Analysis
       |
       +----------------------+
       |                      |
       v                      v
Recovery Probability     Failure Analysis
       |                      |
       +----------+-----------+
                  |
                  v
          Priority Calculation
                  |
                  v
       Recovery Strategy
                  |
        +---------+---------+
        |         |         |
        v         v         v
      Retry    Reminder   Human
      Payment              Review
        |
        v
Recovery Workflow
        |
        v
Revenue Recovery


---

System Architecture

RecoverAI
                       |
        +--------------+--------------+
        |                             |
        v                             v
   Next.js Frontend             FastAPI Backend
        |                             |
        |                             +------------------+
        |                             |                  |
        v                             v                  v
 Dashboard                    Recovery Engine       Razorpay API
        |                             |
        |                             v
        |                     Transaction Analysis
        |                             |
        +-----------------------------+


---

Technology Stack

Frontend

Next.js

React

TypeScript

Tailwind CSS

Lucide React

Razorpay Checkout


Backend

Python

FastAPI

Pydantic

Uvicorn


Payment Integration

Razorpay Test Mode


Configuration

Python python-dotenv

Environment variables



---

Project Structure

RecoverAI/
│
├── backend/
│   ├── main.py
│   ├── AI_Recovery_Model.py
│   ├── requirements.txt
│   ├── .env.example
│   └── ...
│
├── frontend/
│   ├── app/
│   │   └── page.tsx
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   └── ...
│
├── .gitignore
└── README.md


---

Backend

The backend is built using FastAPI.

It provides APIs for:

Transaction analysis

Recovery queue

Transaction retrieval

Dashboard metrics

Razorpay order creation

Razorpay payment verification

Health checking


The backend also contains the recovery decision logic used to evaluate failed transactions.


---

Frontend

The frontend is built using Next.js, React, TypeScript, and Tailwind CSS.

The dashboard provides an interactive interface for:

Analyzing transactions

Viewing AI decisions

Viewing transaction details

Monitoring recovery probability

Viewing expected recovery

Viewing recovery priority

Viewing the recovery queue

Viewing recovery activity

Testing Razorpay payments



---

Razorpay Integration

RecoverAI uses Razorpay Test Mode for payment testing.

The workflow is:

RecoverAI Dashboard
        |
        v
Create Razorpay Order
        |
        v
Razorpay Test Checkout
        |
        +------------------+
        |                  |
        v                  v
Payment Success       Payment Failure
        |                  |
        v                  v
Verify Signature      Recovery Workflow
        |
        v
Payment Verified

The Razorpay secret key is never stored in the frontend source code.

Credentials are loaded through environment variables.


---

Installation and Setup

Prerequisites

Make sure the following are installed:

Python 3.10+

Node.js

npm

Git

A Razorpay Test Mode account



---

Backend Setup

Open a terminal and navigate to the backend:

cd backend

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt


---

Environment Variables

Create a file named:

backend/.env

Add your Razorpay Test Mode credentials:

RAZORPAY_KEY_ID=your_razorpay_test_key_id
RAZORPAY_KEY_SECRET=your_razorpay_test_key_secret

Never commit the .env file to GitHub.

The repository contains .env.example as a safe template.


---

Running the Backend

From the backend directory:

uvicorn main:app --reload

The backend will normally run at:

http://127.0.0.1:8000

FastAPI Swagger documentation will be available at:

http://127.0.0.1:8000/docs


---

Frontend Setup

Open another terminal and navigate to the frontend:

cd frontend

Install dependencies:

npm install


---

Running the Frontend

Start the Next.js development server:

npm run dev

The frontend will normally run at:

http://localhost:3000

Make sure the backend is running before testing the dashboard.


---

API Endpoints

Health Check

GET /health

Checks whether the RecoverAI backend is healthy.


---

Analyze Transaction

POST /analyze

Analyzes a failed payment transaction and returns recovery intelligence.


---

Recovery Queue

POST /recovery-queue

Creates a prioritized recovery queue from transaction data.


---

Get Transactions

GET /transactions

Returns available transaction data.


---

Dashboard Metrics

GET /dashboard-metrics

Returns dashboard-level recovery metrics.


---

Create Razorpay Order

POST /create-order

Creates a Razorpay Test Mode order.


---

Verify Payment

POST /verify-payment

Verifies a Razorpay payment signature.


---

Razorpay Configuration

GET /razorpay-config

Returns the configured Razorpay public key information.


---

Testing the Application

Step 1

Start the backend:

uvicorn main:app --reload

Step 2

Start the frontend:

npm run dev

Step 3

Open:

http://localhost:3000

Step 4

Enter a transaction amount.

Example:

Amount: 5000
Payment Method: UPI
Failure Reason: Network Error

Step 5

Click:

Analyze with RecoverAI

The system displays:

Transaction ID

Recovery probability

Expected recovery

Recovery priority

Failure category

Failure severity

Retry safety

Customer quality

Recovery strategy

Urgency

Priority score

Recommended recovery action

AI reasoning


Step 6

Test the recovery action using:

Execute Recovery Action

Step 7

Use:

Refresh Queue

to update the recovery queue.

Step 8

Use the Razorpay Test Mode integration to test the payment workflow.


---

Screenshots

Dashboard

![RecoverAI Dashboard](screenshots/c:\Users\Niharika\OneDrive\Pictures\Screenshots\Screenshot 2026-09-01 160426.png)

Transaction Analysis

![Transaction Analysis](screenshots/c:\Users\Niharika\OneDrive\Pictures\Screenshots\Screenshot 2026-09-01 160501.png)

Recovery Queue

![Recovery Queue](screenshots/c:\Users\Niharika\OneDrive\Pictures\Screenshots\Screenshot 2026-09-01 160645.png)

Razorpay Test Payment

![Razorpay Test Payment](screenshots/c:\Users\Niharika\OneDrive\Pictures\Screenshots\Screenshot 2026-09-01 160539.png)


---

Security

RecoverAI follows basic security practices for API credentials.

Sensitive credentials are stored using environment variables.

The following files and directories are excluded from Git:

.env
.env.*
venv/
node_modules/
.next/
*.db
*.sqlite

The repository only contains the safe .env.example template.

Razorpay secret credentials should never be placed directly inside frontend code or committed to GitHub.


---

Future Enhancements

The current prototype can be extended with:

Machine learning-based recovery prediction

Historical transaction database

Real-time payment event processing

Webhook-based payment failure detection

Automated recovery campaigns

Email and SMS payment reminders

Customer segmentation

Advanced analytics

Recovery performance tracking

Multi-payment gateway support

Production-grade authentication and authorization

Role-based dashboards

Cloud database integration

Advanced fraud and risk detection

Automated recovery orchestration



---

Use Cases

RecoverAI can be useful for:

E-commerce platforms

Subscription businesses

SaaS companies

Online education platforms

Digital marketplaces

FinTech platforms

Payment platforms

Recurring billing systems


Any business that processes digital payments and experiences payment failures can potentially use a revenue recovery system such as RecoverAI.


---

Project Status

Status: Prototype Completed

Current prototype capabilities include:

Transaction analysis

Recovery probability estimation

Expected recovery calculation

Recovery prioritization

Recovery strategy recommendation

Recovery queue

Dashboard metrics

Transaction monitoring

Recovery activity

Razorpay Test Mode integration

Payment verification

Interactive frontend dashboard



---

Demo

A complete demonstration video will showcase:

1. RecoverAI dashboard


2. Transaction analysis


3. AI recovery decision


4. Recovery priority


5. Recovery queue


6. Recovery action execution


7. Razorpay Test Mode payment


8. Payment verification


9. Recovery workflow



Demo video link will be added here.


---

Team

RecoverAI

Developed as a project for the Razorpay Buildathon 2026.

Contributors

Add the team member names and GitHub profiles here.


---

License

This project is developed as a hackathon prototype.

License information can be added according to the team's preferred open-source or project distribution requirements.


---

Acknowledgements

Razorpay for the payment gateway and Test Mode integration

FastAPI for the backend framework

Next.js and React for the frontend

Tailwind CSS for the UI

Lucide React for interface icons


