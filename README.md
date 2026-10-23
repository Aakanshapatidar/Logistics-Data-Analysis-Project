# UrbanExpress Logistics: Last-Mile Delivery Analysis and Prediction

**Internship Project \| Weeks 1--4**\
**Domain:** E-commerce fulfillment and last-mile logistics\
**Dataset:** 25,000 delivery records\
**Repository:**
https://github.com/Aakanshapatidar/Logistics-Data-Analysis-Project.git

## Project Overview

This project applies a complete data analytics workflow to historical
logistics delivery records. It covers strategic planning and baseline
KPIs, data cleaning and normalization, exploratory data analysis (EDA),
and predictive modeling for delivery-time estimation.

The goal is to turn delivery records into useful evidence for
understanding operational performance, identifying risk patterns, and
supporting better delivery planning. The Week 4 work predicts delivery
duration and flags potentially risky deliveries; it does **not** claim
to implement a live route-optimization system.

## Objectives

-   Establish baseline logistics KPIs and target goals.
-   Inspect and clean the dataset while preserving the raw source.
-   Correct investigated data-representation issues and validate the
    cleaned data.
-   Explore delivery time, cost, distance, weather, region, vehicle,
    partner, and delivery-mode patterns.
-   Train and compare regression models to estimate delivery time.
-   Identify potential delivery-time risks and translate findings into
    operational recommendations.

## Technology Stack

-   **Python**
-   **Pandas and NumPy** --- data manipulation and numerical analysis
-   **Matplotlib and Seaborn** --- charts and exploratory visualization
-   **Scikit-learn** --- preprocessing, regression models,
    cross-validation, and evaluation
-   **Jupyter Notebook / VS Code** --- development
-   **Git and GitHub** --- version control and project hosting

## Dataset Description

The dataset contains 25,000 records and 15 source columns.

  Column                  Description
  ----------------------- ---------------------------------
  `delivery_id`           Delivery identifier
  `delivery_partner`      Delivery service provider
  `package_type`          Package category
  `vehicle_type`          Vehicle used
  `delivery_mode`         Delivery service mode
  `region`                Operating region
  `weather_condition`     Weather condition
  `distance_km`           Delivery distance in kilometres
  `package_weight_kg`     Package weight in kilograms
  `delivery_time_hours`   Actual delivery duration
  `expected_time_hours`   Expected delivery duration
  `delayed`               Source-recorded delay indicator
  `delivery_status`       Delivery outcome/status
  `delivery_rating`       Recorded delivery rating
  `delivery_cost`         Delivery cost

The raw dataset is preserved separately from the cleaned and normalized
outputs.

## Week 1 --- Strategic Planning and Data Exploration

**Objective:** Establish the business problem, define KPIs, and plan the
analytics workflow.

Activities: - Defined the last-mile delivery performance problem. -
Inspected the historical delivery records. - Calculated baseline
delivery, distance, and cost metrics. - Compared baseline performance
with proposed targets. - Proposed predictive regression, spatial
grouping, and route optimization as possible future approaches.

### Baseline KPIs from the Week 1 report

  -----------------------------------------------------------------------
  KPI                                  Baseline                    Target
  ------------------- ------------------------- -------------------------
  On-time delivery     73.32% (18,331 / 25,000)                     ≥ 90%
  rate based on the                             
  source `delayed`                              
  flag                                          

  Average distance                     150.2 km                  ≤ 125 km
  per run                                       

  Average operational                  \$864.00                ≤ \$720.00
  delivery cost                                 
  -----------------------------------------------------------------------

These are the Week 1 report's baseline values. The report uses the
source delay flag to calculate its on-time rate.

## Week 2 --- Data Collection, Cleaning, and Preprocessing

**Objective:** Prepare a reliable dataset for analysis and machine
learning.

Activities: - Inspected dataset dimensions, columns, types, missing
values, and duplicates. - Investigated repeated and corrupted delivery
IDs. - Reconstructed IDs from the sequential row pattern after checking
the surrounding records. - Investigated timestamp-like strings in the
actual and expected delivery-time columns and decoded the encoded values
into numerical hours. - Standardized categorical text. - Checked invalid
numerical values and logical consistency. - Used the IQR method to flag
statistical outliers without automatically deleting potentially valid
long deliveries. - Created a separate Min-Max normalized dataset.

### Data-quality findings documented in the Week 2 report

-   Dataset size: **25,000 rows × 15 columns**
-   Missing cells: **0**
-   Exact duplicate rows: **0**
-   The ID column contained two repeated suspicious values: `250.99` and
    `24750.01`.
-   The two corrupted ID blocks were reconstructed using the expected
    sequential ID pattern.
-   The actual delivery-time column had **203** high-side IQR
    observations above 14 hours; these were retained for further
    business validation.
-   The recorded `delayed` flag disagreed with the simple comparison
    `delivery_time_hours > expected_time_hours` for **1,203** records.

### Week 2 outputs

-   `Delivery_Logistics_Cleaned.csv` --- cleaned values in business
    units.
-   `Delivery_Logistics_Normalized.csv` --- separate Min-Max normalized
    copy of selected numerical variables.

Normalization is intended for analytical/modeling workflows; the cleaned
dataset remains the more interpretable business-unit version.

## Week 3 --- Advanced Data Analysis and Visualization

**Objective:** Explore delivery performance, identify patterns, and
communicate findings using KPIs and charts.

Activities: - Calculated descriptive statistics and logistics KPIs. -
Compared performance across regions, partners, vehicle types, weather,
package types, and delivery modes. - Examined correlations between
numerical variables. - Created visualizations for delivery time, cost,
distance, delays, and operational segments. - Converted findings into
recommendations for further investigation.

### Reported Week 3 KPIs

  KPI                                    Reported value
  ------------------------------------ ----------------
  Total delivery records                         25,000
  Time-based on-time deliveries                  19,534
  Time-based on-time delivery rate               78.14%
  Source-recorded delayed deliveries              6,669
  Source-recorded delay rate                     26.68%
  Average delivery time                      6.25 hours
  Average expected time                     13.11 hours
  Average delivery cost                          864.94
  Average delivery rating                      3.67 / 5
  Average distance                            150.39 km
  Average cost per kilometre                       7.04

**KPI definition note:** The Week 1 source-flag-based on-time rate
(73.32%) and the Week 3 time-based on-time rate (78.14%) use different
definitions. The Week 3 report also documents 1,203 records where the
source delay flag disagrees with the comparison between actual and
expected time. These metrics should therefore be reported separately,
not treated as interchangeable.

### Selected findings reported in Week 3

-   Distance and delivery cost had a strong positive correlation (**r =
    0.991**).
-   Distance and delivery time had a positive correlation (**r =
    0.686**).
-   Stormy-weather deliveries had a reported average delivery time of
    **8.81 hours** and source-recorded delay rate of **41.45%**.
-   Clear-weather deliveries had a reported average delivery time of
    **4.78 hours** and source-recorded delay rate of **17.43%**.
-   Express deliveries had a source-recorded delay rate of **73.78%**
    and time-based on-time rate of **35.33%**.
-   The Central region had the highest reported source-recorded delay
    rate (**27.25%**); East had the lowest (**25.80%**).

These are descriptive findings from the supplied report. Correlation
indicates association, not proof of causation.

### Visualizations

The Week 3 analysis covers: - Delivery status and delivery-time
distribution - Delivery-cost distribution - Distance versus delivery
time and cost - Delay rate by region - Partner and vehicle performance -
Weather impact - Correlation heatmap - Region-by-weather delay
patterns - Package type and delivery time - Delivery mode and cost

## Week 4 --- Predictive Modeling and Optimization

**Objective:** Predict delivery duration using information that can
reasonably be available before or during delivery planning, then use
predictions to flag potential delivery-time risk.

### Modeling workflow

1.  Loaded and validated the cleaned Week 2 dataset.
2.  Set `delivery_time_hours` as the target.
3.  Created `distance_expected_ratio` from distance and expected
    delivery time.
4.  Excluded `delivery_id` as an identifier and excluded `delayed`,
    `delivery_status`, and `delivery_rating` because they are
    outcome-related. `delivery_cost` was also excluded because its
    availability at prediction time was not established.
5.  Used an 80/20 train-test split with `random_state=42`.
6.  Applied median imputation and scaling to numerical features and
    most-frequent imputation plus one-hot encoding to categorical
    features through Scikit-learn pipelines.
7.  Compared a mean baseline, Linear Regression, Decision Tree, Random
    Forest, and Gradient Boosting.
8.  Evaluated predictions using MAE, RMSE, and R², and used 3-fold
    cross-validation to assess stability.
9.  Tuned Gradient Boosting on a reproducible training subset and used
    the tree-based model for feature-importance interpretation.
10. Generated prediction/residual visualizations, risk summaries, and
    analytical scenarios.

### Features used

-   `delivery_partner`
-   `package_type`
-   `vehicle_type`
-   `delivery_mode`
-   `region`
-   `weather_condition`
-   `distance_km`
-   `package_weight_kg`
-   `expected_time_hours`
-   `distance_expected_ratio` (engineered feature)

### Reported Week 4 results

  -----------------------------------------------------------------------
  Model / measure                                         Reported result
  ------------------------------ ----------------------------------------
  Selected final model                                  Linear Regression

  Holdout MAE                                                 1.283 hours

  Holdout RMSE                                                1.622 hours

  Holdout R²                                                        0.728

  3-fold cross-validation MAE                                 1.284 hours

  Tuned Gradient Boosting                                     1.285 hours
  holdout MAE                    

  Tuned Gradient Boosting                                           0.727
  holdout R²                     

  Test-set deliveries flagged as                  1,364 of 5,000 (27.28%)
  potentially risky              
  -----------------------------------------------------------------------

Linear Regression was selected based on its holdout/cross-validation
performance and interpretability. Tuned Gradient Boosting was retained
for tree-based interpretation; the report identifies weather and
distance as dominant features in that interpretation.

**Risk definition:** A test-set delivery was flagged when its predicted
delivery time exceeded its expected delivery time. This is a model-based
risk indicator, not a confirmed observed delay or a measured improvement
in on-time delivery.

**Optimization scope:** The work provides prediction-based risk
screening and analytical scenarios to support planning. It does not
establish that a live vehicle-routing algorithm was implemented or that
actual route distance/cost savings were achieved.

## Recommendations

Based on the supplied analyses:

1.  Use weather-aware planning and consider additional buffers under
    adverse conditions.
2.  Review express-delivery service-level expectations and investigate
    its high reported delay rate.
3.  Use distance-aware delivery planning and investigate opportunities
    to reduce unnecessary travel.
4.  Track partner, vehicle, region, and delivery-mode performance with
    consistently defined KPIs.
5.  Review potentially high-risk predictions before dispatch and
    validate them against operational outcomes.
6.  Investigate the 1,203 source-flag/time-comparison disagreements and
    agree on one documented business definition for delay.
7.  Validate model performance on future data before using predictions
    for operational decisions.

## Limitations

-   The analysis is based on historical records and cannot guarantee
    future performance.
-   Some fields may not be available at the exact moment a prediction
    would be made; feature availability should be confirmed before
    deployment.
-   The source delay flag and time-based definition disagree for some
    records.
-   IQR outliers were flagged for investigation, not automatically
    treated as errors.
-   Model-based risk flags are not the same as observed late deliveries.
-   Route optimization and real-world savings remain proposed
    opportunities unless independently implemented and measured.

## Suggested Repository Structure

Update this tree to match the exact files committed to GitHub:

``` text
Logistics-Data-Analysis-Project/
├── README.md
├── analysis.py
├── Week2_Logistics_Preprocessing.py
├── week3_Logistics_Preprocessing.py
├── week4_ml_logistics.py
├── Delivery_Logistics(5).csv
├── Delivery_Logistics_Cleaned(3).csv
├── Delivery_Logistics_Normalized(2).csv
├── Week1_Strategic_Planning_Logistics_Report.docx
├── Week2_Logistics_Data_Preprocessing_Report.docx
├── Week3_Advanced_Logistics_Analysis_Report.docx
├── Week4_Predictive_Modeling_and_Optimization_Logistics_Report.docx
└── week4_outputs/
    ├── model_comparison.csv
    └── charts and other generated outputs
```

The filenames above reflect the supplied working files, some of which
contain upload-version suffixes such as `(3)` or `(2)`. For a clean
GitHub repository, consider renaming files consistently and updating the
paths in the scripts. Do not include generated outputs in this tree
unless they are committed to the repository.

## How to Run

Install the main dependencies:

``` bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

Run each task's script from the directory containing the required input
CSV, or update each script's input path to match your repository:

``` bash
python analysis.py
python Week2_Logistics_Preprocessing.py
python week3_Logistics_Preprocessing.py
python week4_ml_logistics.py
```

The scripts expect specific input filenames. Ensure the input paths and
filenames in each script match the files in your local repository. The
Week 4 script writes model-comparison and other analysis outputs to
`week4_outputs/`.

## Learning Outcomes

-   Data inspection, cleaning, validation, and normalization
-   Pandas and NumPy for data analysis
-   KPI design and interpretation
-   Exploratory data analysis and visualization
-   Correlation and segment analysis
-   Regression modeling and feature preprocessing
-   Train-test evaluation and cross-validation
-   MAE, RMSE, and R² interpretation
-   Leakage-aware feature selection
-   Prediction-based risk screening
-   Translating analytical results into operational recommendations

## Conclusion

Across four internship tasks, this project progresses from defining
logistics KPIs to preparing data, investigating operational patterns,
and predicting delivery duration. The analyses identify distance,
weather, and delivery-mode performance as useful areas for further
operational investigation. The modeling results provide a starting point
for risk-aware planning, subject to validation on future deliveries and
consistent business definitions.

## Author

**Aakansha Patidar**\
**Project:** UrbanExpress Logistics --- Last-Mile Delivery Analysis and
Prediction\
**GitHub:**
https://github.com/Aakanshapatidar/Logistics-Data-Analysis-Project.git
