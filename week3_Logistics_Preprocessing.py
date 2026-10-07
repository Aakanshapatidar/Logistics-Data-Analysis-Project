
# ============================================================
# WEEK 3: ADVANCED DATA ANALYSIS AND VISUALIZATION IN LOGISTICS
# YuvaIntern Internship Project
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. FOLDER AND FILE SETUP
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# YOUR ACTUAL CLEANED CSV FILE
FILE = os.path.join(
    BASE_DIR,
    "Delivery_Logistics_Cleaned.csv"
)

# Output folders
OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "Week3_Output"
)

CHART_DIR = os.path.join(
    OUTPUT_DIR,
    "charts"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)


# ============================================================
# 2. CHECK CSV FILE
# ============================================================

print("\n" + "=" * 70)
print("WEEK 3 LOGISTICS DATA ANALYSIS")
print("=" * 70)

print("\nChecking CSV file...")

if not os.path.exists(FILE):

    print("\nERROR: CSV file not found!")
    print("Expected file:")
    print(FILE)

    print("\nCSV files available in this folder:")

    csv_files = [
        f for f in os.listdir(BASE_DIR)
        if f.lower().endswith(".csv")
    ]

    if csv_files:
        for f in csv_files:
            print(" -", f)
    else:
        print("No CSV files found.")

    raise FileNotFoundError(FILE)


print("CSV file found successfully!")
print("File:", FILE)


# ============================================================
# 3. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(FILE)

print("\nDataset loaded successfully!")

print("Rows    :", len(df))
print("Columns :", len(df.columns))


# ============================================================
# 4. DISPLAY COLUMN NAMES
# ============================================================

print("\nColumn Names:")

for column in df.columns:
    print(" -", column)


# ============================================================
# 5. BASIC DATA INSPECTION
# ============================================================

print("\n" + "=" * 70)
print("BASIC DATA INSPECTION")
print("=" * 70)

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ============================================================
# 6. CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
)

print("\nCleaned Column Names:")
print(df.columns.tolist())


# ============================================================
# 7. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "delivery_id",
    "delivery_partner",
    "package_type",
    "vehicle_type",
    "delivery_mode",
    "region",
    "weather_condition",
    "distance_km",
    "package_weight_kg",
    "delivery_time_hours",
    "expected_time_hours",
    "delayed",
    "delivery_status",
    "delivery_rating",
    "delivery_cost"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    print("\nERROR: Required columns are missing:")

    for col in missing_columns:
        print(" -", col)

    raise ValueError(
        "Required columns missing from dataset."
    )

print("\nAll required columns are available.")


# ============================================================
# 8. CONVERT NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "distance_km",
    "package_weight_kg",
    "delivery_time_hours",
    "expected_time_hours",
    "delivery_rating",
    "delivery_cost"
]

print("\nConverting numeric columns...")

for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# ============================================================
# 9. CHECK NUMERIC CONVERSION
# ============================================================

print("\nMissing values after numeric conversion:")

print(
    df[numeric_columns].isnull().sum()
)


# ============================================================
# 10. REMOVE INVALID NUMERIC ROWS
# ============================================================

before_rows = len(df)

df = df.dropna(
    subset=numeric_columns
).copy()

after_rows = len(df)

print("\nRows before cleaning :", before_rows)
print("Rows after cleaning  :", after_rows)
print("Rows removed         :", before_rows - after_rows)


# ============================================================
# 11. STANDARDIZE TEXT COLUMNS
# ============================================================

text_columns = [
    "delivery_partner",
    "package_type",
    "vehicle_type",
    "delivery_mode",
    "region",
    "weather_condition",
    "delayed",
    "delivery_status"
]

for col in text_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .str.lower()
    )


# ============================================================
# 12. CREATE CALCULATED COLUMNS
# ============================================================

# Difference between actual and expected time
df["time_difference_hours"] = (
    df["delivery_time_hours"]
    - df["expected_time_hours"]
)


# Calculated delay based on actual vs expected time
df["calculated_delayed"] = np.where(
    df["delivery_time_hours"]
    >
    df["expected_time_hours"],
    "yes",
    "no"
)


# On-time delivery
df["on_time"] = np.where(
    df["delivery_time_hours"]
    <=
    df["expected_time_hours"],
    "yes",
    "no"
)


# Cost per kilometer
df["cost_per_km"] = np.where(
    df["distance_km"] > 0,
    df["delivery_cost"]
    /
    df["distance_km"],
    np.nan
)


# ============================================================
# 13. KEY PERFORMANCE INDICATORS
# ============================================================

total_deliveries = len(df)

on_time_deliveries = (
    df["on_time"]
    .eq("yes")
    .sum()
)

otd_percentage = (
    on_time_deliveries
    /
    total_deliveries
    *
    100
)

recorded_delayed = (
    df["delayed"]
    .eq("yes")
    .sum()
)

recorded_delay_rate = (
    recorded_delayed
    /
    total_deliveries
    *
    100
)

average_delivery_time = (
    df["delivery_time_hours"]
    .mean()
)

average_expected_time = (
    df["expected_time_hours"]
    .mean()
)

average_cost = (
    df["delivery_cost"]
    .mean()
)

average_rating = (
    df["delivery_rating"]
    .mean()
)

average_distance = (
    df["distance_km"]
    .mean()
)

average_cost_per_km = (
    df["cost_per_km"]
    .mean()
)


# ============================================================
# 14. DISPLAY KPI RESULTS
# ============================================================

print("\n" + "=" * 70)
print("KEY PERFORMANCE INDICATORS")
print("=" * 70)

print(
    f"\nTotal Deliveries       : "
    f"{total_deliveries}"
)

print(
    f"On-Time Deliveries     : "
    f"{on_time_deliveries}"
)

print(
    f"Time-Based OTD         : "
    f"{otd_percentage:.2f}%"
)

print(
    f"Recorded Delayed       : "
    f"{recorded_delayed}"
)

print(
    f"Recorded Delay Rate    : "
    f"{recorded_delay_rate:.2f}%"
)

print(
    f"Average Delivery Time : "
    f"{average_delivery_time:.2f} hours"
)

print(
    f"Average Expected Time : "
    f"{average_expected_time:.2f} hours"
)

print(
    f"Average Delivery Cost : "
    f"{average_cost:.2f}"
)

print(
    f"Average Rating        : "
    f"{average_rating:.2f}/5"
)

print(
    f"Average Distance      : "
    f"{average_distance:.2f} km"
)

print(
    f"Average Cost per KM   : "
    f"{average_cost_per_km:.2f}"
)


# ============================================================
# 15. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("DESCRIPTIVE STATISTICS")
print("=" * 70)

statistics = df[
    [
        "distance_km",
        "package_weight_kg",
        "delivery_time_hours",
        "expected_time_hours",
        "delivery_rating",
        "delivery_cost",
        "cost_per_km"
    ]
].describe()

print(statistics)

statistics.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "descriptive_statistics.csv"
    )
)


# ============================================================
# 16. PERFORMANCE FUNCTION
# ============================================================

def performance(group_column):

    result = (
        df.groupby(group_column)
        .agg(
            deliveries=(
                "delivery_id",
                "count"
            ),

            average_delivery_time=(
                "delivery_time_hours",
                "mean"
            ),

            average_expected_time=(
                "expected_time_hours",
                "mean"
            ),

            delay_rate=(
                "delayed",
                lambda x:
                (x == "yes").mean() * 100
            ),

            average_rating=(
                "delivery_rating",
                "mean"
            ),

            average_cost=(
                "delivery_cost",
                "mean"
            ),

            average_distance=(
                "distance_km",
                "mean"
            )
        )
        .reset_index()
    )

    return result


# ============================================================
# 17. REGION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("REGION ANALYSIS")
print("=" * 70)

region_analysis = performance(
    "region"
)

print(region_analysis)

region_analysis.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "region_analysis.csv"
    ),
    index=False
)


# ============================================================
# 18. DELIVERY PARTNER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("DELIVERY PARTNER ANALYSIS")
print("=" * 70)

partner_analysis = performance(
    "delivery_partner"
)

print(partner_analysis)

partner_analysis.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "partner_analysis.csv"
    ),
    index=False
)


# ============================================================
# 19. VEHICLE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("VEHICLE ANALYSIS")
print("=" * 70)

vehicle_analysis = performance(
    "vehicle_type"
)

print(vehicle_analysis)

vehicle_analysis.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "vehicle_analysis.csv"
    ),
    index=False
)


# ============================================================
# 20. WEATHER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("WEATHER ANALYSIS")
print("=" * 70)

weather_analysis = performance(
    "weather_condition"
)

print(weather_analysis)

weather_analysis.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "weather_analysis.csv"
    ),
    index=False
)


# ============================================================
# 21. PACKAGE TYPE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PACKAGE TYPE ANALYSIS")
print("=" * 70)

package_analysis = performance(
    "package_type"
)

print(package_analysis)

package_analysis.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "package_analysis.csv"
    ),
    index=False
)


# ============================================================
# 22. DELIVERY MODE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("DELIVERY MODE ANALYSIS")
print("=" * 70)

mode_analysis = performance(
    "delivery_mode"
)

print(mode_analysis)

mode_analysis.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "delivery_mode_analysis.csv"
    ),
    index=False
)


# ============================================================
# 23. CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CORRELATION ANALYSIS")
print("=" * 70)

correlation_columns = [
    "distance_km",
    "package_weight_kg",
    "delivery_time_hours",
    "expected_time_hours",
    "delivery_rating",
    "delivery_cost",
    "cost_per_km"
]

correlation_matrix = (
    df[correlation_columns]
    .corr()
)

print(correlation_matrix)

correlation_matrix.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "correlation_matrix.csv"
    )
)


# ============================================================
# 24. IMPORTANT CORRELATIONS
# ============================================================

distance_cost_corr = (
    df["distance_km"]
    .corr(
        df["delivery_cost"]
    )
)

distance_time_corr = (
    df["distance_km"]
    .corr(
        df["delivery_time_hours"]
    )
)

rating_otd_corr = (
    df["delivery_rating"]
    .corr(
        df["on_time"]
        .map(
            {
                "yes": 1,
                "no": 0
            }
        )
    )
)

print("\nImportant Correlations:")

print(
    f"Distance vs Cost     : "
    f"{distance_cost_corr:.3f}"
)

print(
    f"Distance vs Time     : "
    f"{distance_time_corr:.3f}"
)

print(
    f"Rating vs OTD        : "
    f"{rating_otd_corr:.3f}"
)


# ============================================================
# 25. DATA QUALITY CHECK
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY CHECK")
print("=" * 70)

print(
    "\nDuplicate Rows:",
    df.duplicated().sum()
)

print(
    "Total Missing Values:",
    df.isnull().sum().sum()
)

print(
    "Negative Distance:",
    (df["distance_km"] < 0).sum()
)

print(
    "Negative Delivery Cost:",
    (df["delivery_cost"] < 0).sum()
)

print(
    "Negative Delivery Time:",
    (df["delivery_time_hours"] < 0).sum()
)


# ============================================================
# 26. RECORDED DELAY VS CALCULATED DELAY
# ============================================================

delay_comparison = pd.crosstab(
    df["delayed"],
    df["calculated_delayed"]
)

print("\n" + "=" * 70)
print("RECORDED DELAY VS CALCULATED DELAY")
print("=" * 70)

print(delay_comparison)

delay_comparison.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "delay_comparison.csv"
    )
)


# ============================================================
# 27. CHART 1 - DELIVERIES BY REGION
# ============================================================

plt.figure(figsize=(10, 6))

region_counts = (
    df["region"]
    .value_counts()
)

region_counts.plot(
    kind="bar"
)

plt.title(
    "Total Deliveries by Region"
)

plt.xlabel("Region")
plt.ylabel("Number of Deliveries")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "01_deliveries_by_region.png"
    )
)

plt.show()


# ============================================================
# 28. CHART 2 - DELAY RATE BY REGION
# ============================================================

plt.figure(figsize=(10, 6))

region_delay = (
    df.groupby("region")["delayed"]
    .apply(
        lambda x:
        (x == "yes").mean() * 100
    )
    .sort_values(
        ascending=False
    )
)

region_delay.plot(
    kind="bar"
)

plt.title(
    "Recorded Delay Rate by Region"
)

plt.xlabel("Region")
plt.ylabel("Delay Rate (%)")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "02_delay_rate_by_region.png"
    )
)

plt.show()


# ============================================================
# 29. CHART 3 - AVERAGE DELIVERY TIME BY PARTNER
# ============================================================

plt.figure(figsize=(10, 6))

partner_time = (
    df.groupby("delivery_partner")
    ["delivery_time_hours"]
    .mean()
    .sort_values(
        ascending=False
    )
)

partner_time.plot(
    kind="bar"
)

plt.title(
    "Average Delivery Time by Delivery Partner"
)

plt.xlabel("Delivery Partner")
plt.ylabel(
    "Average Delivery Time (Hours)"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "03_average_time_by_partner.png"
    )
)

plt.show()


# ============================================================
# 30. CHART 4 - PARTNER DELAY RATE
# ============================================================

plt.figure(figsize=(10, 6))

partner_delay = (
    df.groupby("delivery_partner")
    ["delayed"]
    .apply(
        lambda x:
        (x == "yes").mean() * 100
    )
    .sort_values(
        ascending=False
    )
)

partner_delay.plot(
    kind="bar"
)

plt.title(
    "Recorded Delay Rate by Delivery Partner"
)

plt.xlabel("Delivery Partner")
plt.ylabel("Delay Rate (%)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "04_partner_delay_rate.png"
    )
)

plt.show()


# ============================================================
# 31. CHART 5 - WEATHER VS DELIVERY TIME
# ============================================================

plt.figure(figsize=(10, 6))

weather_time = (
    df.groupby("weather_condition")
    ["delivery_time_hours"]
    .mean()
    .sort_values(
        ascending=False
    )
)

weather_time.plot(
    kind="bar"
)

plt.title(
    "Average Delivery Time by Weather Condition"
)

plt.xlabel("Weather Condition")
plt.ylabel(
    "Average Delivery Time (Hours)"
)

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "05_weather_vs_delivery_time.png"
    )
)

plt.show()


# ============================================================
# 32. CHART 6 - WEATHER VS DELAY RATE
# ============================================================

plt.figure(figsize=(10, 6))

weather_delay = (
    df.groupby("weather_condition")
    ["delayed"]
    .apply(
        lambda x:
        (x == "yes").mean() * 100
    )
    .sort_values(
        ascending=False
    )
)

weather_delay.plot(
    kind="bar"
)

plt.title(
    "Recorded Delay Rate by Weather Condition"
)

plt.xlabel("Weather Condition")
plt.ylabel("Delay Rate (%)")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "06_weather_delay_rate.png"
    )
)

plt.show()


# ============================================================
# 33. CHART 7 - DISTANCE VS DELIVERY COST
# ============================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    df["distance_km"],
    df["delivery_cost"],
    alpha=0.4
)

plt.title(
    "Distance vs Delivery Cost"
)

plt.xlabel(
    "Distance (km)"
)

plt.ylabel(
    "Delivery Cost"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "07_distance_vs_cost.png"
    )
)

plt.show()


# ============================================================
# 34. CHART 8 - DISTANCE VS DELIVERY TIME
# ============================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    df["distance_km"],
    df["delivery_time_hours"],
    alpha=0.4
)

plt.title(
    "Distance vs Delivery Time"
)

plt.xlabel(
    "Distance (km)"
)

plt.ylabel(
    "Delivery Time (Hours)"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "08_distance_vs_delivery_time.png"
    )
)

plt.show()


# ============================================================
# 35. CHART 9 - DELIVERY RATING DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["delivery_rating"],
    bins=10
)

plt.title(
    "Distribution of Delivery Ratings"
)

plt.xlabel(
    "Delivery Rating"
)

plt.ylabel(
    "Number of Deliveries"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "09_rating_distribution.png"
    )
)

plt.show()


# ============================================================
# 36. CHART 10 - COST PER KM BY REGION
# ============================================================

plt.figure(figsize=(10, 6))

cost_region = (
    df.groupby("region")
    ["cost_per_km"]
    .mean()
    .sort_values(
        ascending=False
    )
)

cost_region.plot(
    kind="bar"
)

plt.title(
    "Average Cost per Kilometer by Region"
)

plt.xlabel(
    "Region"
)

plt.ylabel(
    "Cost per KM"
)

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "10_cost_per_km_region.png"
    )
)

plt.show()


# ============================================================
# 37. CHART 11 - DELIVERY TIME DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["delivery_time_hours"],
    bins=30
)

plt.title(
    "Distribution of Delivery Time"
)

plt.xlabel(
    "Delivery Time (Hours)"
)

plt.ylabel(
    "Number of Deliveries"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "11_delivery_time_distribution.png"
    )
)

plt.show()


# ============================================================
# 38. CHART 12 - DELIVERY TIME BY VEHICLE
# ============================================================

plt.figure(figsize=(10, 6))

vehicle_time = (
    df.groupby("vehicle_type")
    ["delivery_time_hours"]
    .mean()
    .sort_values(
        ascending=False
    )
)

vehicle_time.plot(
    kind="bar"
)

plt.title(
    "Average Delivery Time by Vehicle Type"
)

plt.xlabel(
    "Vehicle Type"
)

plt.ylabel(
    "Average Delivery Time (Hours)"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "12_vehicle_delivery_time.png"
    )
)

plt.show()


# ============================================================
# 39. CHART 13 - DELIVERY COST BY DELIVERY MODE
# ============================================================

plt.figure(figsize=(10, 6))

mode_cost = (
    df.groupby("delivery_mode")
    ["delivery_cost"]
    .mean()
    .sort_values(
        ascending=False
    )
)

mode_cost.plot(
    kind="bar"
)

plt.title(
    "Average Delivery Cost by Delivery Mode"
)

plt.xlabel(
    "Delivery Mode"
)

plt.ylabel(
    "Average Cost"
)

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "13_delivery_cost_by_mode.png"
    )
)

plt.show()


# ============================================================
# 40. CHART 14 - BOX PLOT WEATHER VS DELIVERY TIME
# ============================================================

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="weather_condition",
    y="delivery_time_hours"
)

plt.title(
    "Delivery Time Distribution by Weather"
)

plt.xlabel(
    "Weather Condition"
)

plt.ylabel(
    "Delivery Time (Hours)"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "14_boxplot_weather_delivery_time.png"
    )
)

plt.show()


# ============================================================
# 41. CHART 15 - BOX PLOT PACKAGE TYPE VS COST
# ============================================================

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="package_type",
    y="delivery_cost"
)

plt.title(
    "Delivery Cost Distribution by Package Type"
)

plt.xlabel(
    "Package Type"
)

plt.ylabel(
    "Delivery Cost"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "15_boxplot_package_cost.png"
    )
)

plt.show()


# ============================================================
# 42. CHART 16 - CORRELATION HEATMAP
# ============================================================

plt.figure(figsize=(12, 8))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5
)

plt.title(
    "Correlation Heatmap"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "16_correlation_heatmap.png"
    )
)

plt.show()


# ============================================================
# 43. ADVANCED ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("ADVANCED ANALYSIS")
print("=" * 70)


# ============================================================
# 44. TOP 5 PARTNERS BY DELAY RATE
# ============================================================

top_delay_partners = (
    partner_analysis
    .sort_values(
        "delay_rate",
        ascending=False
    )
    .head(5)
)

print("\nTop 5 Partners by Delay Rate:")

print(
    top_delay_partners
)


# ============================================================
# 45. TOP 5 REGIONS BY DELAY RATE
# ============================================================

top_delay_regions = (
    region_analysis
    .sort_values(
        "delay_rate",
        ascending=False
    )
    .head(5)
)

print("\nTop 5 Regions by Delay Rate:")

print(
    top_delay_regions
)


# ============================================================
# 46. WEATHER ANALYSIS
# ============================================================

worst_weather = (
    weather_analysis
    .sort_values(
        "delay_rate",
        ascending=False
    )
)

print("\nWeather Conditions by Delay Rate:")

print(
    worst_weather
)


# ============================================================
# 47. DELIVERY MODE COMPARISON
# ============================================================

print("\nDelivery Mode Comparison:")

print(
    mode_analysis
)


# ============================================================
# 48. SAVE CLEANED ANALYSIS DATA
# ============================================================

cleaned_file = os.path.join(
    OUTPUT_DIR,
    "Week3_Logistics_Cleaned_Analysis.csv"
)

df.to_csv(
    cleaned_file,
    index=False
)

print(
    "\nCleaned analysis dataset saved:"
)

print(
    cleaned_file
)


# ============================================================
# 49. SAVE KPI SUMMARY
# ============================================================

kpi_summary = pd.DataFrame({

    "KPI": [

        "Total Deliveries",

        "On-Time Deliveries",

        "Time-Based OTD Percentage",

        "Recorded Delayed Deliveries",

        "Recorded Delay Rate",

        "Average Delivery Time",

        "Average Expected Time",

        "Average Delivery Cost",

        "Average Rating",

        "Average Distance",

        "Average Cost per KM"
    ],

    "Value": [

        total_deliveries,

        on_time_deliveries,

        round(
            otd_percentage,
            2
        ),

        recorded_delayed,

        round(
            recorded_delay_rate,
            2
        ),

        round(
            average_delivery_time,
            2
        ),

        round(
            average_expected_time,
            2
        ),

        round(
            average_cost,
            2
        ),

        round(
            average_rating,
            2
        ),

        round(
            average_distance,
            2
        ),

        round(
            average_cost_per_km,
            2
        )
    ]
})

kpi_summary.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "kpi_summary.csv"
    ),
    index=False
)


# ============================================================
# 50. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("WEEK 3 ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nKEY FINDINGS")

print(
    f"\n1. Total deliveries analyzed: "
    f"{total_deliveries}"
)

print(
    f"2. Time-Based On-Time Delivery: "
    f"{otd_percentage:.2f}%"
)

print(
    f"3. Recorded delay rate: "
    f"{recorded_delay_rate:.2f}%"
)

print(
    f"4. Average delivery time: "
    f"{average_delivery_time:.2f} hours"
)

print(
    f"5. Average delivery cost: "
    f"{average_cost:.2f}"
)

print(
    f"6. Average delivery rating: "
    f"{average_rating:.2f}/5"
)

print(
    f"7. Distance vs Cost correlation: "
    f"{distance_cost_corr:.3f}"
)

print(
    f"8. Distance vs Delivery Time correlation: "
    f"{distance_time_corr:.3f}"
)

print(
    f"9. Rating vs OTD correlation: "
    f"{rating_otd_corr:.3f}"
)


# ============================================================
# 51. OUTPUT LOCATION
# ============================================================

print("\n" + "=" * 70)
print("OUTPUT FILES")
print("=" * 70)

print(
    "\nAll Week 3 output files:"
)

print(
    OUTPUT_DIR
)

print(
    "\nCharts folder:"
)

print(
    CHART_DIR
)

print("\nGenerated files include:")

print("- kpi_summary.csv")
print("- descriptive_statistics.csv")
print("- region_analysis.csv")
print("- partner_analysis.csv")
print("- vehicle_analysis.csv")
print("- weather_analysis.csv")
print("- package_analysis.csv")
print("- delivery_mode_analysis.csv")
print("- correlation_matrix.csv")
print("- delay_comparison.csv")
print("- Week3_Logistics_Cleaned_Analysis.csv")
print("- 16 visualization charts")

print("\n" + "=" * 70)
print("DONE!")
print("=" * 70)
