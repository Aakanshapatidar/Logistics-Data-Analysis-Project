"""
UrbanExpress Logistics - Week 1: Strategic Baseline Analysis
Dataset Scope: 25,000 Completed Delivery Transactions
"""

import numpy as np
import pandas as pd


def load_raw_dataset(file_path="data/delivery_logistics_dataset.csv"):
    """Loads raw historical telematics dataset."""
    print("Loading raw delivery transactions dataset...")
    df = pd.read_csv(file_path)
    print(f"Total Transactions Loaded: {len(df)}")
    return df


def analyze_baseline_kpis(df):
    """Calculates initial baseline KPIs for strategic planning."""
    # Standardize delay flags for baseline calculation
    df["delayed_clean"] = df["delayed"].astype(str).str.strip().str.lower()
    df["is_delayed"] = df["delayed_clean"].isin(["yes", "1", "true"]).astype(int)

    # Calculate baseline metrics
    total_deliveries = len(df)
    delayed_deliveries = df["is_delayed"].sum()
    on_time_deliveries = total_deliveries - delayed_deliveries

    otd_rate = (on_time_deliveries / total_deliveries) * 100
    late_rate = (delayed_deliveries / total_deliveries) * 100
    avg_distance = df["distance_km"].mean()
    avg_cost = df["delivery_cost"].mean()

    print("\n--- BASELINE KPIS (UNPREPROCESSED DATA) ---")
    print(f"On-Time Delivery (OTD) Rate : {otd_rate:.2f}%")
    print(f"Late Delivery Rate          : {late_rate:.2f}%")
    print(f"Average Route Distance      : {avg_distance:.2f} km")
    print(f"Average Operational Cost    : ${avg_cost:.2f}")

    # Vehicle Type Performance Summary
    print("\n--- BASELINE METRICS BY VEHICLE TYPE ---")
    vehicle_summary = df.groupby("vehicle_type").agg(
        order_count=("order_id", "count"),
        avg_distance_km=("distance_km", "mean"),
        avg_cost_usd=("delivery_cost", "mean"),
        delay_rate=("is_delayed", "mean"),
    )
    print(vehicle_summary)

    return otd_rate, avg_distance, avg_cost


if __name__ == "__main__":
    raw_df = load_raw_dataset()
    analyze_baseline_kpis(raw_df)
    print("\nWeek 1 Strategic Baseline Exploration Completed Successfully.")