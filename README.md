# umkm-ai-business-analyst
AI-powered business analytics assistant for Indonesian e-commerce sellers using Python, Pandas, Langflow, and Google Gemini

# UMKM AI Business Analyst

An AI-powered business analytics assistant designed to help Indonesian e-commerce sellers understand their business performance through transaction data analysis and AI-generated insights.

## Project Overview

Small and medium-sized businesses (UMKM) rely heavily on e-commerce marketplaces to sell their products. However, understanding transaction performance and identifying business improvement opportunities can be challenging.

This project combines Python-based data analytics with a Langflow and Google Gemini-powered AI workflow to transform e-commerce transaction data into actionable business insights.

## Project Objectives

- Analyze e-commerce transaction data.
- Identify order performance and cancellation patterns.
- Explore product category and regional transaction distributions.
- Generate AI-assisted business insights and recommendations.
- Establish a foundation for future marketplace versus independent website feasibility analysis.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data processing |
| Pandas | Data cleaning and analysis |
| Matplotlib | Data visualization |
| Google Colab | Development environment |
| Langflow | AI workflow orchestration |
| Google Gemini | AI-powered business interpretation |

## Dataset

The project uses an Indonesian e-commerce sales dataset containing approximately 18,868 transaction records.

The analysis covers:
- Order information
- Product categories
- Transaction dates
- Payment methods
- Order status
- Customer and regional information

Dataset source: [Insert Kaggle dataset URL]

## Data Analysis

The analysis includes:
- Data inspection and missing-value analysis
- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- Business KPI calculation
- Monthly order and cancellation analysis
- Product category and regional analysis

## AI Agent Architecture

The initial Langflow workflow consists of:

1. Read File: loads transaction data.
2. UMKM Data Analyzer: processes CSV data using Python and Pandas.
3. Prompt Template: combines analytical results with user questions.
4. Google Gemini: interprets business performance and generates recommendations.
5. Chat Output: delivers responses to users.

## Current Capabilities

- Transaction performance analysis
- Order status analysis
- Cancellation rate interpretation
- Regional transaction analysis
- Product category analysis
- AI-generated business recommendations

## Project Limitations

The dataset does not provide complete financial information such as:
- Cost of Goods Sold (COGS)
- Actual marketplace commission fees
- Advertising expenditure
- Website development and maintenance costs
- Independent customer acquisition costs

Therefore, the current version does not establish actual business profitability or determine whether a seller should migrate to an independent website.

## Future Development

- Seller financial profile input
- Marketplace versus website cost comparison
- Multichannel feasibility simulation
- Financial scenario analysis
- More advanced AI-assisted channel strategy recommendations

## Project Status

**Milestone 1: Business Performance Analysis — Implemented**

**Milestone 2: Channel Feasibility Analysis — Planned**

---

Developed as a portfolio project exploring Data Analytics, AI Agents, and business decision support for Indonesian UMKM sellers.
