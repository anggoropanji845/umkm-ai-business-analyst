UMKM AI Business Analyst
An end-to-end descriptive analytics project for Indonesian e-commerce transaction data, combining Python/Pandas calculations with a Langflow-based AI business analyst.
Project objective
Build a data-grounded assistant that helps interpret e-commerce business performance using deterministic Python calculations. The LLM is responsible for explaining the calculated results, not inventing or independently estimating KPI values.
Business questions
- What are the order volume, completion, and cancellation patterns?
- How does Average Order Value (AOV) look when calculated only from completed orders?
- Which months and business segments show different cancellation rates?
- Which product categories appear most frequently across unique orders?
- What additional cost and operational data is required before evaluating an independent sales channel such as a website?
Dataset and scope
The project uses an Indonesia e-commerce cleaned transaction dataset. The analyzed file contains 18,868 records and 19 source columns. The supplied file is already cleaned; the original raw file was not included in this milestone. Therefore, the project does not claim to independently reproduce all earlier raw-data cleaning decisions.

The analysis is descriptive. It does not establish causality, industry benchmarks, net profit, or website financial feasibility. HPP, marketplace fees, operating costs, and complete marketing costs are not available.
Methodology
1. Load and validate the supplied CSV.
2. Check duplicate records, unique order IDs, missing values, and date consistency.
3. Normalize order statuses for analysis.
4. Calculate cancellation rate using cancelled unique orders divided by all unique orders.
5. Calculate AOV using completed orders only; report mean and median.
6. Reindex monthly results so months with no records remain explicit gaps.
7. Analyze cancellation by payment method, province, shipping option, and cancellation reason.
8. Split multi-category cells and count unique orders containing each category.
9. Pass calculated metrics from the Python custom component to the Langflow prompt and LLM.
10. Evaluate agent responses against deterministic Python outputs.
Selected descriptive findings
Metric	Result
Total unique orders	18,868
Completed orders	16,045
Cancelled orders	2,573
Cancellation rate	13.64%
Completed payment total	Rp950,963,704
AOV mean — completed orders	Rp59,268.54
AOV median — completed orders	Rp26,896


Cancellation rate is defined as cancelled unique orders divided by all unique orders. The denominator includes all order statuses.

Monthly examples:
- May 2025: 170 cancellations from 819 orders (20.76%).
- November 2025: 101 cancellations from 1,131 orders (8.93%).
- July 2025: no transaction records in the supplied dataset; cancellation rate is not applicable, not 0%.
These values are descriptive observations, not causal explanations or industry benchmarks.
AI agent architecture
CSV File → UMKM Data Analyzer (Python/Pandas) → Prompt Template → Language Model → Chat Output

Python calculates the KPIs and segments. The LLM interprets the supplied calculations and must disclose unavailable information. This separation reduces reliance on LLM arithmetic.
Agent evaluation
Three manual tests were performed:
- Business overview: partial pass — core KPIs matched, but one payment-zero count was misstated.
- AOV: pass — mean, median, and completed-order filter matched.
- Monthly trend: partial pass — highest and lowest months matched, but December 2023 was incorrectly described as a no-data month.
See [`docs/agent_evaluation.md`](docs/agent_evaluation.md) for the questions, expected values, observed issues, verdicts, and corrective actions. The agent is not yet described as fully validated or hallucination-free.
Repository structure
.
├── README.md
├── data/
│   └── README.md
├── notebooks/
│   └── UMKM_Business_Analysis_Stage1.ipynb
├── langflow/
│   ├── Business_Performance_Analysis_Stage1.json
│   └── UMKMDataAnalyzer_Stage1.py
├── outputs/
│   └── umkm_business_summary_stage1.json
└── docs/
    └── agent_evaluation.md
Do not commit private API keys, credentials, or large/raw datasets unless the dataset license and repository policy explicitly permit redistribution. Add the dataset source URL and license details to data/README.md after verifying the original Kaggle page.
How to reproduce
1. Install the Python packages used by the notebook (pandas, numpy, matplotlib, and nbformat for notebook editing).
2. Place the permitted cleaned CSV in the expected data location and update DATA_PATH in the notebook if needed.
3. Run notebooks/UMKM_Business_Analysis_Stage1.ipynb from top to bottom.
4. Import the Langflow flow JSON or replace the custom component with langflow/UMKMDataAnalyzer_Stage1.py.
5. Configure the model provider credentials inside Langflow; never store credentials in the exported JSON.
6. Run the test questions in docs/agent_evaluation.md and compare answers with the Python summary.
Limitations and next steps
- Audit original date parsing and quantity imputation when the raw dataset is available.
- Expand agent evaluation to at least 8–10 questions and retest the two partial-pass cases.
- Investigate cancellation patterns by reason and segment without claiming causation.
- Review outliers without automatically removing potentially valid bulk orders.
- Build a one-page Power BI dashboard after the analysis definitions are stable.
- Add SQL reproductions of selected KPIs as a complementary skill demonstration.
