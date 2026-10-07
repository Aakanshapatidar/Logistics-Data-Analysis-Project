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

# Logistics Data Analysis Project

## Week 2: Data Collection, Cleaning and Preprocessing

This project focuses on preparing logistics delivery data for further analysis, visualization, and predictive modeling.

The dataset contains 25,000 delivery transactions from a last-mile logistics scenario. The Week 2 task focuses on data quality assessment, cleaning, missing-value analysis, outlier detection, data type correction, normalization, and preprocessing.

---

## Project Overview

**Project:** UrbanExpress Logistics  
**Industry:** E-Commerce Fulfillment & Last-Mile Delivery  
**Dataset:** Delivery Logistics Dataset  
**Records:** 25,000  
**Columns:** 15  

### Main Objectives

- Collect and inspect logistics delivery data
- Identify data quality issues
- Handle incorrect data types
- Check missing values
- Detect duplicate records
- Investigate duplicate delivery IDs
- Correct corrupted delivery IDs
- Convert timestamp-like delivery time values
- Detect numerical outliers
- Validate logical consistency
- Normalize numerical variables
- Prepare clean data for further analysis

---

## Dataset Columns

| Column | Description |
|---|---|
| delivery_id | Unique delivery identifier |
| delivery_partner | Delivery partner |
| package_type | Type of package |
| vehicle_type | Vehicle used for delivery |
| delivery_mode | Delivery mode |
| region | Delivery region |
| weather_condition | Weather during delivery |
| distance_km | Delivery distance |
| package_weight_kg | Package weight |
| delivery_time_hours | Actual delivery time |
| expected_time_hours | Expected delivery time |
| delayed | Delivery delay indicator |
| delivery_status | Delivery status |
| delivery_rating | Customer delivery rating |
| delivery_cost | Delivery cost |

---

## Data Cleaning Performed

The following preprocessing steps were performed:

1. Dataset structure and data types were inspected.
2. Missing values were checked.
3. Duplicate rows were checked.
4. Duplicate delivery IDs were investigated.
5. Suspicious delivery IDs were identified and corrected.
6. Timestamp-like delivery time values were investigated.
7. Delivery and expected time values were converted into numerical hours.
8. Categorical values were standardized using Pandas.
9. Invalid numerical values were checked.
10. Outliers were detected using the IQR method.
11. Logical consistency between delivery time and delay status was checked.
12. Final data validation was performed.

---

## Important Data Quality Findings

### Missing Values

No missing values were found in the dataset.

### Duplicate Rows

No exact duplicate rows were found.

### Duplicate Delivery IDs

Before cleaning, duplicate delivery IDs were detected.

Two suspicious ID values were found:

- `250.99`
- `24750.01`

These values occurred repeatedly and were inconsistent with the expected sequential delivery ID structure.

The delivery IDs were reconstructed using the verified row sequence.

After cleaning:

- Duplicate IDs: **0**
- ID sequence errors: **0**

---

## Delivery Time Correction

The `delivery_time_hours` and `expected_time_hours` columns contained timestamp-like values such as:

```text
1970-01-01 00:00:00.000000008