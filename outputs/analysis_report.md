# Analysis Report — UMKM AI Business Analyst

**Milestone:** 1 — Descriptive Business Analysis  
**Dataset:** Indonesia E-Commerce Sales (cleaned file supplied)  
**Scope note:** Analisis menggunakan file cleaned. File raw sebelum cleaning tidak tersedia untuk memverifikasi ulang imputasi dan parsing awal.

## 1. Executive summary

The supplied cleaned dataset contains **18,868 records**. The analysis identifies **18,868 unique orders**, of which **16,045 are completed** and **2,573 are cancelled**. The overall cancellation rate is **13.64%**, using all unique orders as the denominator.

The mean AOV for completed orders is **Rp59,268.54**, while the median is **Rp26,896**. These are descriptive transaction metrics, not net profit.

## 2. Key performance indicators

| KPI | Result |
|---|---:|
| Total unique orders | 18,868 |
| Completed orders | 16,045 |
| Cancelled orders | 2,573 |
| Cancellation rate | 13.64% |
| Completed payment total | Rp950,963,704 |
| AOV mean — completed orders | Rp59,268.54 |
| AOV median — completed orders | Rp26,896 |
| Average quantity — valid values | 2.54 |
| Median quantity — valid values | 1 |

**Definitions**
- Cancellation rate = cancelled unique orders / all unique orders × 100%.
- AOV is calculated only for orders with normalized status `Selesai`.
- Completed payment total is not net profit; HPP and operating expenses are not available.

## 3. Data quality overview

| Check | Result |
|---|---:|
| Rows | 18,868 |
| Columns in exported analysis dataframe | 25 |
| Duplicate rows | 0 |
| Duplicate order IDs | 0 |
| Date parse failures | 0 |
| Date mismatch count | 0 |
| Missing `total_qty` | 0 |

The `columns` count refers to the dataframe at the point of export, which includes derived analysis columns; it is not necessarily the number of original source CSV columns.

## 4. Monthly cancellation trend

Highest cancellation rate among months with transactions:
- **2025-05** — 20.76% (170 cancelled / 819 orders).

Lowest cancellation rate among months with transactions:
- **2025-11** — 8.93% (101 cancelled / 1,131 orders).

Months with no transaction records in the exported monthly series: **2024-12, 2025-07**. Their cancellation rate is `null` / not applicable, not 0%.

| Month | Total orders | Completed | Cancelled | Cancellation rate |
|---|---:|---:|---:|---:|
| 2023-12 | 444 | 352 | 92 | 20.72% |
| 2024-01 | 431 | 367 | 64 | 14.85% |
| 2024-02 | 389 | 327 | 62 | 15.94% |
| 2024-03 | 453 | 389 | 64 | 14.13% |
| 2024-04 | 492 | 403 | 89 | 18.09% |
| 2024-05 | 620 | 525 | 95 | 15.32% |
| 2024-06 | 697 | 608 | 89 | 12.77% |
| 2024-07 | 1,270 | 1,114 | 156 | 12.28% |
| 2024-08 | 1,293 | 1,097 | 196 | 15.16% |
| 2024-09 | 1,123 | 967 | 156 | 13.89% |
| 2024-10 | 1,217 | 1,058 | 159 | 13.06% |
| 2024-11 | 1,037 | 892 | 145 | 13.98% |
| 2024-12 | 0 | 0 | 0 | N/A |
| 2025-01 | 1,150 | 1,005 | 145 | 12.61% |
| 2025-02 | 957 | 835 | 122 | 12.75% |
| 2025-03 | 628 | 516 | 112 | 17.83% |
| 2025-04 | 824 | 678 | 146 | 17.72% |
| 2025-05 | 819 | 649 | 170 | 20.76% |
| 2025-06 | 615 | 520 | 95 | 15.45% |
| 2025-07 | 0 | 0 | 0 | N/A |
| 2025-08 | 942 | 855 | 87 | 9.24% |
| 2025-09 | 1,131 | 1,016 | 115 | 10.17% |
| 2025-10 | 1,205 | 1,092 | 113 | 9.38% |
| 2025-11 | 1,131 | 780 | 101 | 8.93% |

## 5. Cancellation by payment method

The table below shows the five payment-method groups with the largest order counts in the exported summary. Labels are kept as they appear in the source data; spelling/capitalization variants have not been consolidated.

| Payment method | Total orders | Cancelled | Cancellation rate |
|---|---:|---:|---:|
| COD (Bayar di Tempat) | 10,100 | 1,359 | 13.46% |
| Saldo ShopeePay | 3,209 | 284 | 8.85% |
| Online Payment | 2,754 | 516 | 18.74% |
| SPayLater | 1,303 | 200 | 15.35% |
| SeaBank Bayar Instan | 574 | 80 | 13.94% |

## 6. Cancellation by province

The following are the first five province groups in the exported ranking, which uses a minimum group size of 30 orders. These are descriptive rates, not evidence that province causes cancellations.

| Province | Total orders | Cancelled | Cancellation rate |
|---|---:|---:|---:|
| SULAWESI UTARA | 38 | 13 | 34.21% |
| SULAWESI TENGAH | 49 | 16 | 32.65% |
| KALIMANTAN TIMUR | 129 | 37 | 28.68% |
| NUSA TENGGARA BARAT (NTB) | 97 | 27 | 27.84% |
| KALIMANTAN TENGAH | 123 | 31 | 25.20% |

## 7. Cancellation reasons

Top recorded cancellation reasons among cancelled orders:

| Reason | Cancelled orders |
|---|---:|
| Dibatalkan oleh Pembeli. Alasan: Lainnya/ berubah pikiran | 604 |
| Dibatalkan oleh Pembeli. Alasan: Ubah Pesanan yang Ada | 500 |
| Dibatalkan secara otomatis oleh sistem. Alasan: Pesanan belum dibayar | 403 |
| Dibatalkan oleh Pembeli. Alasan: Need to change delivery address | 280 |
| Dibatalkan secara otomatis oleh sistem. Alasan: Pengiriman gagal | 238 |

## 8. Product categories

Top categories by number of unique orders containing the category. One order may contain more than one category; these values are not units sold.

| Category | Unique orders containing category |
|---|---:|
| Celengan | 5,420 |
| Mangkok Sambal / Saus | 3,562 |
| Aksesoris Pintu | 2,571 |
| Nampan / Tray | 1,320 |
| Other | 827 |

## 9. Interpretation and limitations

1. The mean AOV is higher than the median, suggesting that the distribution of completed-order values is right-skewed. This is a descriptive interpretation, not a causal finding.
2. Monthly cancellation rates vary over time. The dataset does not provide an external industry benchmark, so the rates should not be labelled objectively high or low.
3. Segment-level differences do not establish causation. Sample sizes should be considered before prioritizing operational actions.
4. The dataset does not provide HPP, complete marketplace fees, or operating costs. Net profit and financial feasibility of an independent website cannot be calculated.
5. This report is generated from the supplied cleaned CSV summary. The original raw dataset is needed to audit earlier cleaning and imputation decisions.

## 10. Relationship to the JSON output

This Markdown report is the human-readable presentation of selected fields from `umkm_business_summary_stage1.json`. The JSON remains the structured output for Python and the Langflow agent. If the analysis is rerun, regenerate both outputs from the same run so that the report and JSON remain consistent.
