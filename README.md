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

# Week 3: Advanced Data Analysis and Visualization in Logistics

## 📌 Project Overview

This project is part of my **Week 3 Internship Task: Advanced Data Analysis and Visualization in Logistics**.

The objective of this project is to analyze logistics delivery data using Python and identify patterns related to delivery time, delays, cost, distance, weather, delivery partners, vehicles, regions, and delivery modes.

The analysis includes **Exploratory Data Analysis (EDA), Logistics KPI Analysis, Correlation Analysis, Data Visualization, Bottleneck Identification, and Business Recommendations**.

---

## 📂 Dataset

**Dataset:** `Delivery_Logistics_Cleaned(2).csv`

The dataset contains **25,000 delivery records and 15 variables**.

### Important Variables

- `delivery_id` — Unique delivery identifier
- `delivery_partner` — Delivery service provider
- `package_type` — Type of package
- `vehicle_type` — Vehicle used for delivery
- `delivery_mode` — Delivery service mode
- `region` — Delivery region
- `weather_condition` — Weather during delivery
- `distance_km` — Delivery distance
- `package_weight_kg` — Package weight
- `delivery_time_hours` — Actual delivery time
- `expected_time_hours` — Expected delivery time
- `delayed` — Recorded delay indicator
- `delivery_status` — Delivery status
- `delivery_rating` — Delivery/customer rating
- `delivery_cost` — Delivery cost

---

## 🛠️ Tools and Technologies

- **Python**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **Seaborn**
- **Jupyter Notebook / VS Code**
- **Git & GitHub**

---

## 🔍 Analysis Performed

### 1. Data Inspection

The dataset was examined for:

- Number of rows and columns
- Column names
- Data types
- Missing values
- Duplicate records
- Unique values
- Numerical statistics
- Categorical distributions

### 2. Data Preparation

The following analytical fields were created:

- `delayed_flag`
- `on_time_flag`
- `cost_per_km`

An on-time delivery was defined as:

```text
delivery_time_hours <= expected_time_hours
```

The original dataset was not overwritten.

---

## 📊 Logistics KPIs

The project calculates:

| KPI | Result |
|---|---:|
| Total Deliveries | 25,000 |
| On-Time Deliveries | 19,534 |
| Time-Based OTD | 78.14% |
| Recorded Delayed Deliveries | 6,669 |
| Recorded Delay Rate | 26.68% |
| Average Delivery Time | 6.25 hours |
| Average Expected Time | 13.11 hours |
| Average Delivery Cost | 864.94 |
| Average Rating | 3.67 / 5 |
| Average Distance | 150.39 km |
| Average Cost per KM | 7.04 |

> **Note:** The recorded `delayed` field and the calculated time-based OTD measure are not identical. Both metrics are therefore reported separately.

---

## 📈 Visualizations

The project includes the following visualizations:

1. Delivery Performance Status
2. Delivery Time Distribution
3. Delivery Cost Distribution
4. Distance vs Delivery Time
5. Distance vs Delivery Cost
6. Delay Rate by Region
7. Delivery Partner Performance
8. Vehicle Type Performance
9. Weather Impact on Delivery Performance
10. Correlation Heatmap
11. Region × Weather Delay Analysis
12. Package Type × Delivery Time
13. Delivery Mode × Cost

All charts are generated using Python and saved as image files.

---

## 🔗 Correlation Analysis

Important relationships identified include:

- **Distance vs Delivery Cost:** `r = 0.991`
- **Distance vs Delivery Time:** `r = 0.686`

These correlations indicate associations between the variables and should not be interpreted as proof of causation.

---

## 🚨 Key Findings

### Weather Impact

Stormy weather shows:

- Average delivery time: **8.81 hours**
- Recorded delay rate: **41.45%**

Clear weather shows:

- Average delivery time: **4.78 hours**
- Recorded delay rate: **17.43%**

### Delivery Mode

Express deliveries show:

- Recorded delay rate: **73.78%**
- Time-based OTD: **35.33%**

This makes express delivery the most significant service-risk segment identified in the analysis.

### Regional Performance

- Highest recorded delay rate: **Central — 27.25%**
- Lowest recorded delay rate: **East — 25.80%**

### Delivery Partner

Xpressbees shows:

- Recorded delay rate: **28.27%**
- Average rating: **3.61**

FedEx shows comparatively strong performance:

- Average delivery time: **6.14 hours**
- Recorded delay rate: **25.16%**
- Average rating: **3.70**

### Distance and Cost

Distance and delivery cost have a very strong positive relationship with:

```text
Correlation = 0.991
```

This indicates that distance is closely associated with delivery cost in the dataset.

---

## 💡 Recommendations

Based on the analysis, the following recommendations are proposed:

1. Implement **weather-aware logistics planning**.
2. Review **express delivery SLAs and expected delivery targets**.
3. Optimize routes to reduce unnecessary distance and transportation cost.
4. Develop delivery-partner performance scorecards.
5. Monitor Central region for recurring delay patterns.
6. Use vehicle type as a supporting factor rather than the sole allocation criterion.
7. Standardize the definition of logistics KPIs.
8. Monitor performance by weather, region, partner, delivery mode, and distance.

---

## 📁 Project Structure

```text
Logistics-Data-Analysis-Project/
│
├── Delivery_Logistics_Cleaned(2).csv
│
├── week3_logistics_analysis.py
│
├── Week3_Advanced_Logistics_Analysis_Report.docx
│
├── Week3_Submission_Description.txt
│
├── descriptive_statistics.csv
├── logistics_kpis.csv
├── correlation_matrix.csv
│
├── region_performance.csv
├── delivery_partner_performance.csv
├── vehicle_type_performance.csv
├── weather_condition_performance.csv
├── package_type_performance.csv
├── delivery_mode_performance.csv
│
└── charts/
    ├── 01_delivery_status.png
    ├── 02_delivery_time_distribution.png
    ├── 03_delivery_cost_distribution.png
    ├── 04_distance_vs_time.png
    ├── 05_distance_vs_cost.png
    ├── 06_delay_by_region.png
    ├── 07_partner_performance.png
    ├── 08_vehicle_performance.png
    ├── 09_weather_impact.png
    ├── 10_correlation_heatmap.png
    ├── 11_region_weather_delay.png
    ├── 12_package_type_time.png
    └── 13_mode_cost.png
```

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Logistics-Data-Analysis-Project
```

### 2. Install required libraries

```bash
pip install pandas numpy matplotlib seaborn
```

### 3. Run the analysis

```bash
python week3_logistics_analysis.py
```

The analysis will generate the required tables and visualization outputs.

---

## 🎯 Learning Outcomes

Through this project, I developed practical skills in:

- Data validation
- Data preprocessing
- Exploratory Data Analysis
- Pandas and NumPy
- KPI calculation
- Group-by analysis
- Correlation analysis
- Data visualization
- Logistics performance analysis
- Bottleneck identification
- Business insight generation
- Data-driven decision-making

---

## 🏁 Conclusion

This project demonstrates how logistics data can be transformed into actionable operational insights.

The analysis identified **weather conditions, express delivery performance, delivery distance, regional variation, and partner performance** as important areas for further monitoring.

The project also demonstrates the importance of using clearly defined KPIs and validating the underlying data before making operational decisions.

---

## 👩‍💻 Author

**Aakansha Patidar**

**Project:** Week 3 – Advanced Data Analysis and Visualization in Logistics