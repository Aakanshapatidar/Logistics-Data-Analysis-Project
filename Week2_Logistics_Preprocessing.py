import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

INPUT = "Delivery_Logistics(4).csv"

df = pd.read_csv(INPUT, low_memory=False)

# ---------------- Initial inspection ----------------
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 10 rows:")
print(df.head(10))
print("\nData types:")
print(df.dtypes)
print("\nDescriptive statistics:")
print(df.describe(include="all"))
print("\nMissing values:")
print(df.isna().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nDuplicate IDs:", df["delivery_id"].duplicated().sum())

# ---------------- Delivery ID investigation/repair ----------------
expected_id = pd.Series(np.arange(1, len(df) + 1), index=df.index)
first_corrupt = df["delivery_id"].eq(250.99)
last_corrupt = df["delivery_id"].eq(24750.01)
id_mismatch = df["delivery_id"].ne(expected_id)

# The raw file has exactly 250 occurrences of each suspicious value,
# and the surrounding rows confirm a sequential 1..25000 ID pattern.
if first_corrupt.sum() == 250 and last_corrupt.sum() == 250 and id_mismatch.sum() == 500:
    df.loc[first_corrupt, "delivery_id"] = expected_id[first_corrupt]
    df.loc[last_corrupt, "delivery_id"] = expected_id[last_corrupt]
else:
    raise ValueError("delivery_id corruption pattern differs from the investigated dataset.")

df["delivery_id"] = df["delivery_id"].astype("int64")

# ---------------- Timestamp-like hour correction ----------------
def decode_hour_column(series):
    dt = pd.to_datetime(series, errors="coerce")
    if dt.isna().any():
        raise ValueError("Unexpected value in encoded hour column.")
    # In this dataset, the nanosecond integer itself encodes the intended hour.
    return dt.astype("int64").astype("int64")

for col in ["delivery_time_hours", "expected_time_hours"]:
    df[col] = decode_hour_column(df[col])

# ---------------- Categorical cleaning ----------------
categorical_cols = [
    "delivery_partner", "package_type", "vehicle_type", "delivery_mode",
    "region", "weather_condition", "delayed", "delivery_status"
]
for col in categorical_cols:
    df[col] = df[col].astype("string").str.strip().str.lower()

# ---------------- Missing-value treatment ----------------
# Actual dataset has no missing values, so these guarded rules do not change it.
numeric_cols = [
    "distance_km", "package_weight_kg", "delivery_time_hours",
    "expected_time_hours", "delivery_rating", "delivery_cost"
]
for col in numeric_cols:
    if df[col].isna().any():
        df[col] = df[col].fillna(df[col].median())

for col in categorical_cols:
    if df[col].isna().any():
        df[col] = df[col].fillna("unknown")

# ---------------- Duplicate rows ----------------
df = df.drop_duplicates()

# ---------------- Invalid-value checks ----------------
print("\nInvalid value checks:")
print("Distance <= 0:", int((df["distance_km"] <= 0).sum()))
print("Weight <= 0:", int((df["package_weight_kg"] <= 0).sum()))
print("Rating outside 1-5:", int(((df["delivery_rating"] < 1) | (df["delivery_rating"] > 5)).sum()))
print("Cost <= 0:", int((df["delivery_cost"] <= 0).sum()))

# ---------------- IQR outlier detection ----------------
def detect_outliers_iqr(data, column):
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mask = (data[column] < lower) | (data[column] > upper)

    print(f"\n{column}")
    print("Q1:", q1)
    print("Q3:", q3)
    print("IQR:", iqr)
    print("Lower bound:", lower)
    print("Upper bound:", upper)
    print("Outliers:", int(mask.sum()))
    return mask

for col in [
    "distance_km", "package_weight_kg", "delivery_time_hours",
    "expected_time_hours", "delivery_rating", "delivery_cost"
]:
    detect_outliers_iqr(df, col)

# ---------------- Logical consistency ----------------
time_late = df["delivery_time_hours"] > df["expected_time_hours"]
delay_flag = df["delayed"].eq("yes")

print("\nLogical checks:")
print("Actual time > expected time:", int(time_late.sum()))
print("Delayed = yes:", int(delay_flag.sum()))
print("Time-vs-delay mismatches:", int(time_late.ne(delay_flag).sum()))

status_consistent = (
    (df["delayed"].eq("no") & df["delivery_status"].eq("delivered")) |
    (df["delayed"].eq("yes") & df["delivery_status"].isin(["delayed", "failed"]))
)
print("Delay/status inconsistencies:", int((~status_consistent).sum()))

# ---------------- Normalization ----------------
normalized = df.copy()
normalize_cols = [
    "distance_km", "package_weight_kg", "delivery_time_hours",
    "expected_time_hours", "delivery_cost"
]
scaler = MinMaxScaler()
normalized[normalize_cols] = scaler.fit_transform(normalized[normalize_cols])

# ---------------- Final validation ----------------
print("\nFINAL VALIDATION")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("Missing cells:", int(df.isna().sum().sum()))
print("Duplicate rows:", int(df.duplicated().sum()))
print("Duplicate IDs:", int(df["delivery_id"].duplicated().sum()))
print("ID sequence errors:", int(df["delivery_id"].ne(np.arange(1, len(df)+1)).sum()))
print("\nData types:")
print(df.dtypes)

# ---------------- Export ----------------
df.to_csv("Delivery_Logistics_Cleaned.csv", index=False)
normalized.to_csv("Delivery_Logistics_Normalized.csv", index=False)
print("\nExport complete.")
