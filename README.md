# UrbanExpress Logistics: Last-Mile Delivery Optimization

## Executive Overview
UrbanExpress Logistics manages last-mile order fulfillment across 5 metropolitan operating zones (Central, East, North, South, West) using a multi-modal fleet of 6 vehicle types. 

This project establishes a data-driven framework utilizing **Data Cleaning**, **Exploratory Analytics**, **Supervised Regression**, and **Route Optimization** to solve core operational bottlenecks across 25,000 historical order transactions.

## Week 1 Verified Baseline Metrics vs. Target Goals

| KPI Metric | Baseline Value (Raw Data) | Target Goal | Primary Impact |
| :--- | :--- | :--- | :--- |
| **On-Time Delivery Rate (OTD)** | 73.32% (18,331 / 25,000) | ≥ 90.0% | Customer Satisfaction |
| **Average Distance per Run** | 150.2 km | ≤ 125.0 km | Fuel & Maintenance Savings |
| **Average Operational Delivery Cost** | $864.00 | ≤ $720.00 | Increased Profit Margin |

## Repository Architecture
- `data/`: Contains raw delivery logs (25,000 records).
- `docs/`: Strategic planning reports and deliverables.
- `analysis.py`: Week 1 script for raw baseline data exploration and KPI verification.