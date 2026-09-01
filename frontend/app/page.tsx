"use client";

import { useEffect, useState } from "react";
import Script from "next/script";

import {
  ArrowUpRight,
  BrainCircuit,
  DollarSign,
  ShieldCheck,
  TrendingUp,
  Users,
  Target,
  CreditCard,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
} from "lucide-react";

declare global {
  interface Window {
    Razorpay: any;
  }
}

const BACKEND_URL = "http://127.0.0.1:8000";

export default function Home() {

  const [analysis, setAnalysis] = useState<any>(null);

  const [loading, setLoading] = useState(false);

  const [actionLoading, setActionLoading] = useState(false);

  const [actionStatus, setActionStatus] = useState("");

  const [paymentLoading, setPaymentLoading] = useState(false);

  const [paymentStatus, setPaymentStatus] = useState("");

  const [activities, setActivities] = useState<string[]>([]);

  const [recoveryQueue, setRecoveryQueue] = useState<any[]>([]);

  const [queueLoading, setQueueLoading] = useState(false);

  const [transactions, setTransactions] = useState<any[]>([]);

  const [metrics, setMetrics] = useState<any>(null);

  const [transactionId, setTransactionId] = useState("");

  const [transactionDetails, setTransactionDetails] = useState({
    amount: 0,
    payment_method: "",
    failure_reason: "",
  });


  // ============================================================
  // LOAD DASHBOARD
  // ============================================================

  const loadDashboard = async () => {

    try {

      const [
        queueResponse,
        transactionResponse,
        metricsResponse,
      ] = await Promise.all([

        fetch(`${BACKEND_URL}/recovery-queue`),

        fetch(`${BACKEND_URL}/transactions`),

        fetch(`${BACKEND_URL}/dashboard-metrics`),
      ]);


      if (queueResponse.ok) {

        const queueData =
          await queueResponse.json();

        setRecoveryQueue(
          queueData.recovery_queue || []
        );
      }


      if (transactionResponse.ok) {

        const transactionData =
          await transactionResponse.json();

        setTransactions(
          transactionData.transactions || []
        );
      }


      if (metricsResponse.ok) {

        const metricsData =
          await metricsResponse.json();

        setMetrics(metricsData);
      }

    } catch (error) {

      console.error(
        "Dashboard loading error:",
        error
      );
    }
  };


  // ============================================================
  // INITIAL LOAD
  // ============================================================

  useEffect(() => {

    loadDashboard();

  }, []);


  // ============================================================
  // ANALYZE
  // ============================================================

  const analyzeTransaction = async () => {

    const amountInput =
      document.getElementById(
        "amount"
      ) as HTMLInputElement;

    const methodInput =
      document.getElementById(
        "payment_method"
      ) as HTMLSelectElement;

    const reasonInput =
      document.getElementById(
        "failure_reason"
      ) as HTMLSelectElement;


    const amount =
      Number(amountInput.value);


    if (!amount || amount <= 0) {

      alert(
        "Please enter a valid transaction amount."
      );

      return;
    }


    setLoading(true);

    setAnalysis(null);

    setActionStatus("");


    try {

      const response =
        await fetch(
          `${BACKEND_URL}/analyze`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({

              amount,

              payment_method:
                methodInput.value,

              payment_status:
                "failed",

              failure_reason:
                reasonInput.value,

              attempt_count:
                1,

              checkout_abandoned:
                0,

              checkout_duration_seconds:
                180,

              previous_transactions:
                10,

              previous_successful_transactions:
                9,

              previous_success_rate:
                0.9,

              is_subscription:
                0,

              days_overdue:
                0,
            }),
          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Analysis failed"
        );
      }


      
      const newTransactionId =
  data.transaction_id ||
  data.id ||
  data.transaction?.transaction_id ||
  data.transaction?.id ||
  "";

setTransactionId(newTransactionId);


      setTransactionDetails({

        amount,

        payment_method:
          methodInput.value,

        failure_reason:
          reasonInput.value,
      });


      setAnalysis(
        data.analysis
      );


      setActivities(
        previous => [

          `AI analyzed ${data.transaction_id} — ${data.analysis.recovery_probability}% recovery probability`,

          ...previous,
        ]
      );


      await loadDashboard();

    } catch (error) {

      console.error(
        "Analysis error:",
        error
      );

      alert(
        "Unable to analyze transaction. Check whether backend is running."
      );

    } finally {

      setLoading(false);
    }
  };


  // ============================================================
  // EXECUTE RECOVERY
  // ============================================================

  const executeRecoveryAction = async () => {

  if (!analysis) {
    setActionStatus("Please analyze a transaction first.");
    return;
  }

  if (!transactionId) {
    setActionStatus(
      "Transaction ID is missing. Please analyze the transaction again."
    );
    return;
  }

  setActionLoading(true);
  setActionStatus("");

  try {

    const response = await fetch(
      `${BACKEND_URL}/execute-recovery`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          transaction_id: transactionId,
          action: analysis.recommended_action,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail ||
        data.message ||
        "Recovery action failed"
      );
    }

    setActionStatus(
      data.message ||
      `Recovery action "${formatText(
        analysis.recommended_action
      )}" executed successfully.`
    );

    setActivities(previous => [
      `Recovery action executed for ${transactionId} — ${formatText(
        analysis.recommended_action
      )}`,
      ...previous,
    ]);

    await loadDashboard();

  } catch (error: any) {

    console.error(
      "Recovery action error:",
      error
    );

    setActionStatus(
      error.message ||
      "Recovery action failed."
    );

  } finally {

    setActionLoading(false);

  }
};


  // ============================================================
  // REFRESH QUEUE
  // ============================================================

  // ============================================================
// REFRESH QUEUE
// ============================================================

const loadRecoveryQueue = async () => {

  setQueueLoading(true);

  try {

    const response = await fetch(
      `${BACKEND_URL}/recovery-queue`
    );

    const data = await response.json();

    if (!response.ok) {

      throw new Error(
        data.detail ||
        "Failed to refresh recovery queue"
      );

    }

    setRecoveryQueue(
      data.recovery_queue || []
    );

    setActivities(previous => [

      "Recovery queue refreshed — highest-value opportunities identified",

      ...previous,

    ]);

  } catch (error: any) {

    console.error(
      "Recovery queue error:",
      error
    );

    setActivities(previous => [

      `Recovery queue refresh failed — ${
        error.message ||
        "Unknown error"
      }`,

      ...previous,

    ]);

  } finally {

    setQueueLoading(false);

  }

};



  // ============================================================
  // RAZORPAY
  // ============================================================

  const testPaymentWithRazorpay =
    async () => {

      if (!analysis) {

        alert(
          "Please analyze a transaction first."
        );

        return;
      }


      if (!window.Razorpay) {

        alert(
          "Razorpay Checkout is still loading. Please wait a moment and try again."
        );

        return;
      }


      setPaymentLoading(true);

      setPaymentStatus("");


      try {

        const orderResponse =
          await fetch(
            `${BACKEND_URL}/create-order`,
            {
              method: "POST",

              headers: {
                "Content-Type":
                  "application/json",
              },

              body: JSON.stringify({

                amount:
                  transactionDetails.amount,
              }),
            }
          );


        const orderData =
          await orderResponse.json();


        if (!orderResponse.ok) {

          throw new Error(
            orderData.detail ||
            "Order creation failed"
          );
        }


        const options = {

          key:
            orderData.key_id,

          amount:
            orderData.amount,

          currency:
            orderData.currency,

          name:
            "RecoverAI",

          description:
            "RecoverAI Test Payment",

          order_id:
            orderData.order_id,


          handler:
            async function (
              response: any
            ) {

              try {

                const verifyResponse =
                  await fetch(
                    `${BACKEND_URL}/verify-payment`,
                    {
                      method: "POST",

                      headers: {
                        "Content-Type":
                          "application/json",
                      },

                      body: JSON.stringify({

                        razorpay_order_id:
                          response.razorpay_order_id,

                        razorpay_payment_id:
                          response.razorpay_payment_id,

                        razorpay_signature:
                          response.razorpay_signature,
                      }),
                    }
                  );


                const verifyData =
                  await verifyResponse.json();


                if (!verifyResponse.ok) {

                  throw new Error(
                    verifyData.detail ||
                    "Payment verification failed"
                  );
                }


                setPaymentStatus(
                  `Payment successful and verified. Payment ID: ${response.razorpay_payment_id}`
                );


                setActivities(
                  previous => [

                    "Razorpay test payment completed and verified successfully",

                    ...previous,
                  ]
                );

              } catch (error) {

                console.error(
                  "Payment verification error:",
                  error
                );

                setPaymentStatus(
                  "Payment completed, but verification failed."
                );

              } finally {

                setPaymentLoading(false);
              }
            },


          modal: {

            ondismiss:
              function () {

                setPaymentLoading(false);

                setPaymentStatus(
                  "Razorpay payment window was closed."
                );
              },
          },


          theme: {

            color:
              "#2563eb",
          },
        };


        const razorpay =
          new window.Razorpay(
            options
          );


        razorpay.on(
          "payment.failed",
          function (
            response: any
          ) {

            console.error(
              "Razorpay payment failed:",
              response
            );


            setPaymentStatus(
              "Test payment failed. RecoverAI can analyze the failure and recommend a recovery action."
            );


            setActivities(
              previous => [

                "Razorpay test payment failed — recovery workflow triggered",

                ...previous,
              ]
            );


            setPaymentLoading(false);
          }
        );


        razorpay.open();

      } catch (error: any) {

        console.error(
          "Razorpay error:",
          error
        );


        setPaymentStatus(
          error.message ||
          "Order creation failed."
        );


        setPaymentLoading(false);
      }
    };


  return (

    <main className="min-h-screen bg-slate-950 text-white">

      <Script
        src="https://checkout.razorpay.com/v1/checkout.js"
        strategy="afterInteractive"
      />


      {/* =====================================================
          NAVBAR
      ===================================================== */}

      <nav className="border-b border-slate-800 bg-slate-950/90">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-5">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600">

              <BrainCircuit size={22} />

            </div>

            <div>

              <h1 className="text-xl font-bold">
                RecoverAI
              </h1>

              <p className="text-xs text-slate-400">
                Intelligent Revenue Recovery
              </p>

            </div>

          </div>


          <div className="hidden gap-6 text-sm text-slate-300 md:flex">

            <span className="text-white">
              Dashboard
            </span>

            <span>
              Transactions
            </span>

            <span>
              Recovery
            </span>

            <span>
              Analytics
            </span>

          </div>

        </div>

      </nav>


      {/* =====================================================
          CONTENT
      ===================================================== */}

      <section className="mx-auto max-w-7xl px-8 py-10">


        <div className="mb-10">

          <p className="mb-2 text-sm font-medium text-blue-400">
            AI-POWERED REVENUE RECOVERY
          </p>

          <h2 className="text-4xl font-bold">

            Recover more revenue.

            <span className="text-blue-500">
              {" "}Automatically.
            </span>

          </h2>

          <p className="mt-3 max-w-2xl text-slate-400">

            RecoverAI analyzes failed payments,
            predicts recovery probability,
            prioritizes recovery opportunities,
            and recommends safe recovery actions.

          </p>

        </div>


        {/* =====================================================
            DYNAMIC STATS
        ===================================================== */}

        <div className="grid gap-5 md:grid-cols-4">

          <StatCard

            title="Revenue at Risk"

            value={
              metrics
                ? `₹${Number(
                    metrics.revenue_at_risk
                  ).toLocaleString("en-IN")}`
                : "₹0"
            }

            change="Live"

            icon={
              <DollarSign size={20} />
            }
          />


          <StatCard

            title="Expected Recovery"

            value={
              metrics
                ? `₹${Number(
                    metrics.expected_recoverable_revenue
                  ).toLocaleString("en-IN")}`
                : "₹0"
            }

            change="AI"

            icon={
              <TrendingUp size={20} />
            }
          />


          <StatCard

            title="Active Cases"

            value={
              metrics
                ? String(
                    metrics.total_cases
                  )
                : "0"
            }

            change="Live"

            icon={
              <Users size={20} />
            }
          />


          <StatCard

            title="Avg Recovery Probability"

            value={
              metrics
                ? `${metrics.average_recovery_probability}%`
                : "0%"
            }

            change="AI"

            icon={
              <BrainCircuit size={20} />
            }
          />

        </div>


        {/* =====================================================
            ANALYZE
        ===================================================== */}

        <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/20 text-blue-400">

              <BrainCircuit size={21} />

            </div>

            <div>

              <h3 className="text-lg font-semibold">
                Analyze a Transaction
              </h3>

              <p className="text-sm text-slate-400">

                RecoverAI will save the transaction
                and add it to the recovery queue.

              </p>

            </div>

          </div>


          <div className="mt-6 grid gap-4 md:grid-cols-3">

            <input
              id="amount"
              type="number"
              placeholder="Amount"
              className="rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-blue-500"
            />


            <select
              id="payment_method"
              defaultValue="UPI"
              className="rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none"
            >

              <option value="UPI">
                UPI
              </option>

              <option value="CARD">
                Card
              </option>

              <option value="NETBANKING">
                Net Banking
              </option>

              <option value="WALLET">
                Wallet
              </option>

            </select>


            <select
              id="failure_reason"
              defaultValue="network_error"
              className="rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none"
            >

              <option value="network_error">
                Network Error
              </option>

              <option value="bank_error">
                Bank Error
              </option>

              <option value="insufficient_funds">
                Insufficient Funds
              </option>

              <option value="technical_error">
                Technical Error
              </option>

              <option value="timeout">
                Timeout
              </option>

            </select>

          </div>


          <button

            onClick={
              analyzeTransaction
            }

            disabled={loading}

            className="mt-5 rounded-xl bg-blue-600 px-6 py-3 font-medium hover:bg-blue-500 disabled:opacity-60"
          >

            {loading
              ? "Analyzing..."
              : "Analyze with RecoverAI"}

          </button>


          {/* ===================================================
              ANALYSIS
          =================================================== */}

          {analysis && (

            <div className="mt-6 rounded-2xl border border-blue-500/20 bg-slate-950 p-6">

              <div className="mb-6 flex items-center justify-between">

                <div>

                  <p className="text-xs uppercase tracking-wider text-slate-500">
                    Transaction
                  </p>

                  <p className="mt-1 font-mono text-sm text-slate-300">
                    #{transactionId}
                  </p>

                </div>


                <div className="rounded-full bg-blue-500/10 px-3 py-1 text-xs text-blue-400">
                  AI Analyzed
                </div>

              </div>


              <div className="grid gap-4 md:grid-cols-3">

                <InfoCard
                  title="Amount"
                  value={`₹${transactionDetails.amount.toLocaleString("en-IN")}`}
                />

                <InfoCard
                  title="Payment Method"
                  value={transactionDetails.payment_method}
                />

                <InfoCard
                  title="Failure Reason"
                  value={formatText(transactionDetails.failure_reason)}
                />

              </div>


              {/* AI RESULT */}

              <div className="mt-6 grid gap-4 md:grid-cols-3">

                <ResultCard

                  title="Recovery Probability"

                  value={`${analysis.recovery_probability}%`}

                />


                <ResultCard

                  title="Expected Recovery"

                  value={analysis.recovery_potential}

                />


                <ResultCard

                  title="Priority"

                  value={analysis.recovery_priority}

                />

              </div>


              {/* INTELLIGENCE */}

              <div className="mt-5 rounded-2xl border border-blue-500/20 bg-blue-500/5 p-5">

                <div className="flex items-center gap-3">

                  <BrainCircuit
                    size={20}
                    className="text-blue-400"
                  />

                  <div>

                    <p className="font-semibold">
                      RecoverAI Decision Intelligence
                    </p>

                    <p className="text-xs text-slate-500">
                      AI-generated recovery decision
                    </p>

                  </div>

                </div>


                <div className="mt-5 grid gap-4 md:grid-cols-4">

                  <InfoCard
                    title="Failure Category"
                    value={formatText(analysis.failure_category)}
                  />

                  <InfoCard
                    title="Severity"
                    value={analysis.failure_severity}
                  />

                  <InfoCard
                    title="Retry Safety"
                    value={analysis.retry_safety}
                  />

                  <InfoCard
                    title="Customer Quality"
                    value={analysis.customer_quality}
                  />

                </div>


                <div className="mt-4 grid gap-4 md:grid-cols-3">

                  <InfoCard
                    title="Recovery Strategy"
                    value={formatText(analysis.recovery_strategy)}
                  />

                  <InfoCard
                    title="Urgency"
                    value={analysis.urgency}
                  />

                  <InfoCard
                    title="Priority Score"
                    value={`${analysis.priority_score}/100`}
                  />

                </div>


                <div className="mt-4 rounded-xl bg-slate-950/70 p-4">

                  <p className="text-xs uppercase tracking-wider text-slate-500">
                    AI Reasoning
                  </p>

                  <p className="mt-2 text-sm leading-6 text-slate-400">
                    {analysis.strategy_reason}
                  </p>

                </div>

              </div>


              {/* RECOMMENDED ACTION */}

              <div className="mt-5 rounded-xl border border-slate-800 bg-slate-900 p-5">

                <p className="text-sm text-slate-400">
                  Recommended Recovery Action
                </p>

                <p className="mt-2 text-xl font-bold">
                  {formatText(
                    analysis.recommended_action
                  )}
                </p>

                <p className="mt-3 text-sm leading-6 text-slate-400">
                  {analysis.reason}
                </p>

              </div>


              {/* RAZORPAY */}

              <div className="mt-5 rounded-2xl border border-blue-500/20 bg-blue-500/5 p-5">

                <div className="flex items-center gap-3">

                  <CreditCard
                    size={20}
                    className="text-blue-400"
                  />

                  <div>

                    <p className="font-semibold">
                      Test Payment with Razorpay
                    </p>

                    <p className="text-xs text-slate-500">
                      Test-mode payment recovery workflow
                    </p>

                  </div>

                </div>


                <button

                  onClick={
                    testPaymentWithRazorpay
                  }

                  disabled={paymentLoading}

                  className="mt-5 w-full rounded-xl bg-blue-600 px-6 py-3 font-semibold hover:bg-blue-500 disabled:opacity-60"
                >

                  {paymentLoading
                    ? "Opening Razorpay..."
                    : "Test Payment with Razorpay"}

                </button>


                {paymentStatus && (

                  <div className="mt-4 rounded-xl border border-slate-800 bg-slate-950 p-4">

                    <div className="flex items-center gap-2">

                      {paymentStatus.includes(
                        "verified"
                      ) ? (

                        <CheckCircle2
                          size={18}
                          className="text-green-400"
                        />

                      ) : (

                        <AlertCircle
                          size={18}
                          className="text-yellow-400"
                        />

                      )}

                      <p className="text-sm font-medium">
                        Razorpay Payment Status
                      </p>

                    </div>

                    <p className="mt-2 text-sm text-slate-400">
                      {paymentStatus}
                    </p>

                  </div>

                )}

              </div>


              {/* EXECUTE */}

              <button

                onClick={
                  executeRecoveryAction
                }

                disabled={actionLoading}

                className="mt-5 w-full rounded-xl bg-blue-600 px-6 py-3 font-medium hover:bg-blue-500 disabled:opacity-60"
              >

                {actionLoading
                  ? "Executing Recovery Action..."
                  : "Execute Recovery Action"}

              </button>


              {actionStatus && (

                <div className="mt-4 rounded-xl border border-green-500/20 bg-green-500/5 p-4">

                  <div className="flex items-center gap-2 text-green-400">

                    <ShieldCheck size={17} />

                    Recovery action processed

                  </div>

                  <p className="mt-2 text-sm text-slate-400">
                    {actionStatus}
                  </p>

                </div>

              )}

            </div>

          )}

        </div>


        {/* =====================================================
            TRANSACTIONS
        ===================================================== */}

        <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <div className="mb-6 flex items-center justify-between">

            <div>

              <h3 className="text-lg font-semibold">
                Recent Transactions
              </h3>

              <p className="text-sm text-slate-400">
                Transactions analyzed by RecoverAI
              </p>

            </div>


            <button

              onClick={
                loadDashboard
              }

              className="flex items-center gap-2 text-sm text-blue-400"
            >

              <RefreshCw size={15} />

              Refresh

            </button>

          </div>


          {transactions.length === 0 ? (

            <div className="rounded-xl border border-dashed border-slate-800 p-8 text-center">

              <p className="text-sm text-slate-500">
                No transactions analyzed yet.
              </p>

            </div>

          ) : (

            <div className="space-y-3">

              {transactions
                .slice(0, 8)
                .map(
                  (item) => (

                    <div

                      key={
                        item.transaction_id ||
                        item.id
                      }

                      className="grid grid-cols-5 items-center gap-4 rounded-xl border border-slate-800 bg-slate-950/50 p-4"
                    >

                      <div>

                        <p className="text-sm font-medium">
                          {item.transaction_id || item.id || "N/A"}
                        </p>

                        <p className="text-xs text-slate-500">
                          {item.payment_method}
                        </p>

                      </div>


                      <p className="text-sm font-semibold">
                        ₹{Number(
                          item.amount
                        ).toLocaleString("en-IN")}
                      </p>


                      <p className="text-sm font-semibold">
                        {item.recovery_probability}%
                      </p>


                      <span className="w-fit rounded-full bg-blue-500/10 px-3 py-1 text-xs text-blue-400">

                        {item.recovery_priority}

                      </span>


                      <p className="text-right text-xs text-slate-400">
                        {formatText(
                          item.recommended_action
                        )}
                      </p>

                    </div>

                  )
                )}

            </div>

          )}

        </div>


        {/* =====================================================
            RECOVERY QUEUE
        ===================================================== */}

        <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <div className="flex items-center justify-between">

            <div>

              <h3 className="text-lg font-semibold">
                Recovery Queue
              </h3>

              <p className="text-sm text-slate-400">
                Highest-priority recovery opportunities
              </p>

            </div>


            <button

              onClick={
                loadRecoveryQueue
              }

              disabled={queueLoading}

              className="rounded-xl bg-white px-4 py-2 text-sm font-semibold text-black disabled:opacity-50"
            >

              {queueLoading
                ? "Refreshing..."
                : "Refresh Queue"}

            </button>

          </div>


          {recoveryQueue.length === 0 ? (

            <div className="mt-5 rounded-xl border border-dashed border-slate-800 p-8 text-center">

              <p className="text-sm text-slate-500">
                No recovery opportunities yet.
              </p>

              <p className="mt-1 text-xs text-slate-600">
                Analyze transactions to populate the queue.
              </p>

            </div>

          ) : (

            <div className="mt-5 space-y-3">

              {recoveryQueue.map(
                (item) => (

                  <div

                    key={
                      item.transaction_id ||
                      item.id
                    }

                    className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950/70 p-4"
                  >

                    <div className="flex items-center gap-4">

                      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-800 text-sm font-bold">

                        #{item.rank}

                      </div>


                      <div>

                        <p className="text-sm font-semibold">
                          {item.transaction_id || item.id || "N/A"}
                        </p>

                        <p className="text-xs text-slate-500">

                          ₹{Number(
                            item.amount
                          ).toLocaleString("en-IN")}

                          {" • "}

                          {item.payment_method}

                        </p>

                      </div>

                    </div>


                    <div className="text-right">

                      <p className="text-sm font-semibold">
                        {item.recovery_probability}%
                      </p>

                      <p className="text-xs text-slate-500">

                        ₹{Number(
                          item.expected_recoverable_revenue
                        ).toLocaleString("en-IN")}

                        {" "}recoverable

                      </p>

                    </div>

                  </div>

                )
              )}

            </div>

          )}

        </div>


        {/* =====================================================
            ACTIVITY
        ===================================================== */}

        <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <div className="mb-6 flex items-center justify-between">

            <div>

              <h3 className="text-lg font-semibold">
                Recovery Activity
              </h3>

              <p className="text-sm text-slate-400">
                Recent RecoverAI decisions
              </p>

            </div>


            <div className="rounded-full bg-green-500/10 px-3 py-1 text-xs text-green-400">
              Live
            </div>

          </div>


          {activities.length === 0 ? (

            <div className="rounded-xl border border-dashed border-slate-800 p-6 text-center">

              <p className="text-sm text-slate-500">
                No activity yet.
              </p>

            </div>

          ) : (

            <div className="space-y-3">

              {activities
                .slice(0, 8)
                .map(
                  (
                    activity,
                    index
                  ) => (

                    <div

                      key={index}

                      className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-950/50 p-4"
                    >

                      <div className="h-2 w-2 rounded-full bg-blue-400" />

                      <p className="text-sm text-slate-300">
                        {activity}
                      </p>

                    </div>

                  )
                )}

            </div>

          )}

        </div>

      </section>

    </main>
  );
}


/* ============================================================
   HELPERS
============================================================ */

function formatText(
  value: string
) {

  if (!value)
    return "";

  return value
    .replaceAll("_", " ")
    .replace(
      /\b\w/g,
      char =>
        char.toUpperCase()
    );
}


/* ============================================================
   INFO CARD
============================================================ */

function InfoCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {

  return (

    <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">

      <p className="text-xs uppercase tracking-wider text-slate-500">
        {title}
      </p>

      <p className="mt-2 text-lg font-semibold">
        {value}
      </p>

    </div>
  );
}


/* ============================================================
   RESULT CARD
============================================================ */

function ResultCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {

  return (

    <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">

      <p className="text-sm text-slate-400">
        {title}
      </p>

      <p className="mt-2 text-2xl font-bold text-blue-400">
        {value}
      </p>

    </div>
  );
}


/* ============================================================
   STAT CARD
============================================================ */

function StatCard({
  title,
  value,
  change,
  icon,
}: {
  title: string;
  value: string;
  change: string;
  icon: React.ReactNode;
}) {

  return (

    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

      <div className="flex items-center justify-between">

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600/15 text-blue-400">

          {icon}

        </div>

        <span className="text-xs text-green-400">
          {change}
        </span>

      </div>


      <p className="mt-5 text-sm text-slate-400">
        {title}
      </p>


      <p className="mt-1 text-2xl font-bold">
        {value}
      </p>

    </div>
  );
}