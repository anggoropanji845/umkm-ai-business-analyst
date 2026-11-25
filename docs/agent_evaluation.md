# Agent Evaluation — UMKM AI Business Analyst

**Milestone:** 1 — Descriptive Business Analysis  
**Evaluation type:** Manual factual validation against the Python/Pandas business summary  
**Dataset:** `clean-indonesia_ecommerce_cleaned.csv`  
**Evaluation status:** 2 tests pass/partial-pass, 1 test partial-pass. The agent is not yet considered fully validated.

## 1. Evaluation objective

This evaluation checks whether the Langflow agent:
1. Reports numerical metrics consistently with the Python analyzer.
2. Uses the intended KPI definitions.
3. Distinguishes facts from interpretations and hypotheses.
4. Preserves time-series gaps and does not invent or misstate periods.
5. Avoids unsupported causal claims.

The Python analyzer and its exported `umkm_business_summary_stage1.json` are the reference for calculated values. The LLM is expected to interpret those values, not independently recalculate them.

## 2. Test cases and results

### Test 01 — Business overview

**Question**

> Berikan ringkasan performa bisnis berdasarkan dataset yang tersedia. Tampilkan total orders, completed orders, cancelled orders, dan cancellation rate. Jelaskan juga bagaimana cancellation rate tersebut dihitung.

**Expected values**

| Metric | Expected result |
|---|---:|
| Total orders | 18,868 |
| Completed orders | 16,045 |
| Cancelled orders | 2,573 |
| Cancellation rate | 13.64% |
| Completed payment sum | Rp950,963,704 |
| AOV mean (completed only) | Rp59,268.54 |
| AOV median (completed only) | Rp26,896 |

Cancellation rate definition: cancelled unique orders divided by all unique orders, multiplied by 100. The denominator includes all order statuses.

**Observed result**

The agent reported the main order counts, cancellation rate, completed payment sum, and AOV values correctly. It also correctly explained that the cancellation-rate denominator includes all order statuses.

**Issue found**

The agent stated that there were 283 orders with zero payment. This is incorrect.

- 283 records have `Metode Pembayaran = Unknown`.
- 2,573 cancelled orders have `Total Pembayaran = 0`.

**Verdict: PARTIAL PASS**

The main KPIs are correct, but the agent confused two different data-quality/payment observations. The response must be corrected before being used as a fully validated example.

---

### Test 02 — Average Order Value

**Question**

> Berapa Average Order Value (AOV) bisnis ini? Tampilkan mean dan median. Jelaskan mengapa kedua metrik tersebut perlu diperhatikan dan status pesanan apa yang digunakan dalam perhitungan.

**Expected values**

| Metric | Expected result |
|---|---:|
| AOV mean | Rp59,268.54 |
| AOV median | Rp26,896 |
| Included order status | `Selesai` only |
| Completed orders | 16,045 |

**Observed result**

The agent returned the expected mean and median, specified that AOV uses completed orders only, and excluded cancelled orders from the AOV calculation. Its explanation of the difference between mean and median was consistent with the observed distribution.

**Verdict: PASS**

No material numerical or methodological issue was identified in this response.

---

### Test 03 — Monthly cancellation trend

**Question**

> Analisis tren pembatalan pesanan berdasarkan bulan. Identifikasi bulan dengan cancellation rate tertinggi dan terendah. Sertakan jumlah order dan jumlah pembatalan sebagai konteks.

**Expected values**

| Period | Total orders | Completed | Cancelled | Cancellation rate |
|---|---:|---:|---:|---:|
| December 2023 | 444 | 352 | 92 | 20.72% |
| May 2025 | 819 | 649 | 170 | 20.76% |
| July 2025 | 0 | 0 | 0 | N/A |
| August 2025 | 942 | 855 | 87 | 9.24% |
| September 2025 | 1,131 | 1,016 | 115 | 10.17% |
| October 2025 | 1,205 | 1,092 | 113 | 9.38% |
| November 2025 | 1,131 | 780 | 101 | 8.93% |

**Observed result**

The agent correctly identified May 2025 as the highest cancellation-rate month (20.76%) and November 2025 as the lowest (8.93%). It also correctly described the November counts.

**Issues found**

1. The agent incorrectly described December 2023 as a month with zero orders. The reference summary contains 444 orders and 92 cancelled orders for December 2023.
2. July 2025 is the zero-order gap in the supplied dataset. A zero-order month must have a null/not-applicable cancellation rate, not a 0% cancellation rate.
3. The response should not label December 2023 as a gap or omit its actual observations when discussing the time series.

**Verdict: PARTIAL PASS**

The highest and lowest months are correct, but the temporal interpretation contains a factual error. The agent must be retested after the prompt or analyzer context is improved.

---

## 3. Consolidated evaluation

| Test | Result | Main finding |
|---|---|---|
| Test 01 — Business overview | Partial pass | Main KPIs correct; confuses 283 Unknown payment methods with zero-payment orders |
| Test 02 — AOV | Pass | Mean, median, and completed-order filter correct |
| Test 03 — Monthly trend | Partial pass | Highest/lowest months correct; incorrectly calls December 2023 a data gap |

**Overall conclusion**

The agent demonstrates that it can use the Python-generated KPI summary for several core metrics. However, the current evaluation does not support claiming that the agent is fully accurate or hallucination-free. Two factual inconsistencies were found in the three manual tests.

The evaluation set should be expanded to 8–10 questions. Each answer should be checked against a deterministic Pandas result, including edge cases such as missing months, status normalization, payment-method segments, and cancellation reasons.

## 4. Corrective actions

1. Strengthen the analyzer output with explicit, separately named fields:
   - `unknown_payment_method_count`
   - `cancelled_orders_with_zero_payment`
   - `monthly_trend` with zero-order months represented using `cancellation_rate_pct: null`.
2. Add a prompt rule: never infer that a month is missing from a partial excerpt; use the exact month-level records supplied by Python.
3. Require the agent to distinguish `Unknown` payment method from `Total Pembayaran = 0`.
4. Retest Test 01 and Test 03 after updating the component/prompt.
5. Add at least five more tests before describing the agent as validated.

## 5. Scope and limitations

This is a manual evaluation with three questions, not a statistically representative benchmark of all possible user prompts. Passing these tests does not prove that the agent is hallucination-free.

The dataset supplied for this milestone is already cleaned. The original raw dataset is required to audit the earlier missing-value imputation and original date-parsing process.
