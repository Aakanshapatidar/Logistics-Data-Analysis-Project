"""
Week 4: Predictive Modeling and Optimization in Logistics Systems
Dataset: Delivery_Logistics_Cleaned.csv

This script:
1. Loads and validates the cleaned Week 2 dataset
2. Prevents target leakage
3. Engineers distance_expected_ratio
4. Splits data 80/20
5. Trains baseline, Linear Regression, Decision Tree, Random Forest, Gradient Boosting
6. Evaluates MAE, RMSE, R2
7. Performs 3-fold CV
8. Tunes Gradient Boosting with a small GridSearchCV on a reproducible 5,000-row training subset
9. Selects Linear Regression as final model based on holdout/CV performance and interpretability
10. Uses tuned Gradient Boosting for tree-based feature importance
11. Generates actual-vs-predicted and residual plots
12. Generates model-based potential-delay risk
13. Produces segment risk tables and analytical scenarios
14. Exports all results
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = "Delivery_Logistics_Cleaned.csv"
OUTPUT_DIR = "week4_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# 1. Load and validate
# -----------------------------
df = pd.read_csv(DATA_PATH)

required_columns = [
    "delivery_id", "delivery_partner", "package_type", "vehicle_type",
    "delivery_mode", "region", "weather_condition", "distance_km",
    "package_weight_kg", "delivery_time_hours", "expected_time_hours",
    "delayed", "delivery_status", "delivery_rating", "delivery_cost"
]

missing_required = [c for c in required_columns if c not in df.columns]
if missing_required:
    raise ValueError(f"Missing required columns: {missing_required}")

print("Shape:", df.shape)
print("Missing cells:", int(df.isna().sum().sum()))
print("Duplicate rows:", int(df.duplicated().sum()))
print("\\nData types:\\n", df.dtypes)

# -----------------------------
# 2. Target analysis
# -----------------------------
target = "delivery_time_hours"
print("\\nTarget statistics:\\n", df[target].describe())

q1 = df[target].quantile(0.25)
q3 = df[target].quantile(0.75)
iqr = q3 - q1
upper = q3 + 1.5 * iqr
outliers = int((df[target] > upper).sum())
print("IQR upper bound:", upper)
print("High-side IQR outliers:", outliers)

# -----------------------------
# 3. Leakage-safe feature set
# -----------------------------
# Excluded:
# delayed, delivery_status, delivery_rating = outcome/post-delivery information
# delivery_cost = timing availability is not established; keep only for descriptive analysis
# delivery_id = identifier, not a predictive feature

df["distance_expected_ratio"] = (
    df["distance_km"] / df["expected_time_hours"].replace(0, np.nan)
)
df["distance_expected_ratio"] = df["distance_expected_ratio"].replace(
    [np.inf, -np.inf], np.nan
)

features = [
    "delivery_partner", "package_type", "vehicle_type", "delivery_mode",
    "region", "weather_condition", "distance_km", "package_weight_kg",
    "expected_time_hours", "distance_expected_ratio"
]

X = df[features]
y = df[target]

categorical_features = [c for c in features if X[c].dtype == "object"]
numeric_features = [c for c in features if c not in categorical_features]

# Sparse pipeline: appropriate for Linear Regression / tree ensembles
pre_sparse = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]), numeric_features),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ]), categorical_features)
])

# Dense pipeline: used for Gradient Boosting and feature importance
pre_dense = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]), numeric_features),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ]), categorical_features)
])

# -----------------------------
# 4. Train/test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

print("\\nTrain size:", len(X_train))
print("Test size:", len(X_test))

# -----------------------------
# 5. Baseline
# -----------------------------
baseline_pred = np.repeat(y_train.mean(), len(y_test))

# -----------------------------
# 6. Models
# -----------------------------
models = {
    "Linear Regression": Pipeline([
        ("pre", pre_sparse),
        ("model", LinearRegression())
    ]),
    "Decision Tree": Pipeline([
        ("pre", pre_sparse),
        ("model", DecisionTreeRegressor(
            random_state=42, max_depth=12, min_samples_leaf=5
        ))
    ]),
    "Random Forest": Pipeline([
        ("pre", pre_sparse),
        ("model", RandomForestRegressor(
            random_state=42,
            n_estimators=100,
            max_depth=18,
            min_samples_leaf=2,
            max_features=0.8,
            n_jobs=-1
        ))
    ]),
    "Gradient Boosting": Pipeline([
        ("pre", pre_dense),
        ("model", GradientBoostingRegressor(
            random_state=42,
            n_estimators=100,
            learning_rate=0.05,
            max_depth=3,
            min_samples_leaf=5
        ))
    ])
}

predictions = {}
fitted_models = {}

results = []

def evaluate(name, actual, predicted):
    return {
        "Model": name,
        "MAE": mean_absolute_error(actual, predicted),
        "RMSE": mean_squared_error(actual, predicted) ** 0.5,
        "R2": r2_score(actual, predicted)
    }

results.append(evaluate("Baseline", y_test, baseline_pred))

for name, pipe in models.items():
    print(f"\\nTraining {name}...")
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    predictions[name] = pred
    fitted_models[name] = pipe
    results.append(evaluate(name, y_test, pred))

metrics = pd.DataFrame(results)

# -----------------------------
# 7. Cross-validation
# -----------------------------
cv = KFold(n_splits=3, shuffle=True, random_state=42)
cv_mae = {"Baseline": []}

for train_idx, val_idx in cv.split(X_train):
    fold_mean = y_train.iloc[train_idx].mean()
    fold_pred = np.repeat(fold_mean, len(val_idx))
    cv_mae["Baseline"].append(
        mean_absolute_error(y_train.iloc[val_idx], fold_pred)
    )

cv_mae = {"Baseline": float(np.mean(cv_mae["Baseline"]))}

for name, pipe in models.items():
    scores = cross_val_score(
        pipe, X_train, y_train, cv=cv,
        scoring="neg_mean_absolute_error", n_jobs=1
    )
    cv_mae[name] = float((-scores).mean())

metrics["CV_MAE"] = metrics["Model"].map(cv_mae)
metrics.to_csv(os.path.join(OUTPUT_DIR, "model_comparison.csv"), index=False)

print("\\nMODEL COMPARISON")
print(metrics.round(4))

# -----------------------------
# 8. Tune strongest tree-based candidate
# -----------------------------
# Gradient Boosting had the strongest tree-based CV performance.
# To keep tuning reasonable, use a reproducible 5,000-row subset.
train_for_tuning = pd.concat([X_train, y_train.rename(target)], axis=1)
tune_n = min(5000, len(train_for_tuning))
tune_df = train_for_tuning.sample(n=tune_n, random_state=42)

tune_X = tune_df[features]
tune_y = tune_df[target]

base_gb = Pipeline([
    ("pre", pre_dense),
    ("model", GradientBoostingRegressor(random_state=42))
])

param_grid = {
    "model__n_estimators": [80, 120],
    "model__learning_rate": [0.05, 0.08],
    "model__max_depth": [2, 3],
    "model__min_samples_leaf": [5]
}

grid = GridSearchCV(
    base_gb,
    param_grid=param_grid,
    cv=3,
    scoring="neg_mean_absolute_error",
    n_jobs=1
)
grid.fit(tune_X, tune_y)

print("\\nBest Gradient Boosting parameters:")
print(grid.best_params_)
print("Best tuning CV MAE:", -grid.best_score_)

tuned_gb = Pipeline([
    ("pre", pre_dense),
    ("model", GradientBoostingRegressor(
        random_state=42,
        n_estimators=grid.best_params_["model__n_estimators"],
        learning_rate=grid.best_params_["model__learning_rate"],
        max_depth=grid.best_params_["model__max_depth"],
        min_samples_leaf=grid.best_params_["model__min_samples_leaf"]
    ))
])

tuned_gb.fit(X_train, y_train)
tuned_pred = tuned_gb.predict(X_test)
tuned_result = evaluate("Tuned Gradient Boosting", y_test, tuned_pred)
print("\\nTuned Gradient Boosting:", {k: round(v, 4) if isinstance(v, float) else v for k,v in tuned_result.items()})

# -----------------------------
# 9. Final model selection
# -----------------------------
# Linear Regression is selected because it has the best overall holdout MAE/RMSE/R2
# and excellent CV stability, while remaining highly interpretable.
final_model = fitted_models["Linear Regression"]
final_pred = predictions["Linear Regression"]

print("\\nFINAL MODEL: Linear Regression")
print(evaluate("Linear Regression", y_test, final_pred))

# -----------------------------
# 10. Feature importance from tuned tree model
# -----------------------------
feature_names = tuned_gb.named_steps["pre"].get_feature_names_out()
importance_values = tuned_gb.named_steps["model"].feature_importances_

importance_df = pd.DataFrame({
    "encoded_feature": feature_names,
    "importance": importance_values
})

def original_feature(encoded_name):
    if encoded_name.startswith("num__"):
        return encoded_name.split("__", 1)[1]
    rest = encoded_name.split("__", 1)[1]
    for col in categorical_features:
        if rest.startswith(col + "_"):
            return col
    return rest

importance_df["feature"] = importance_df["encoded_feature"].map(original_feature)
feature_importance = (
    importance_df.groupby("feature", as_index=False)["importance"]
    .sum()
    .sort_values("importance", ascending=False)
)
feature_importance["importance_pct"] = (
    100 * feature_importance["importance"] / feature_importance["importance"].sum()
)
feature_importance.to_csv(
    os.path.join(OUTPUT_DIR, "feature_importance.csv"), index=False
)

print("\\nFeature importance:")
print(feature_importance.round(4))

# -----------------------------
# 11. Actual vs predicted + residuals
# -----------------------------
test_results = df.loc[X_test.index].copy()
test_results["predicted_delivery_time_hours"] = final_pred
test_results["residual_actual_minus_predicted"] = (
    test_results[target] - test_results["predicted_delivery_time_hours"]
)

test_results["potential_delay"] = (
    test_results["predicted_delivery_time_hours"]
    > test_results["expected_time_hours"]
)

test_results.to_csv(
    os.path.join(OUTPUT_DIR, "test_predictions_and_risk.csv"),
    index=False
)

plt.figure(figsize=(7, 6))
plt.scatter(y_test, final_pred, s=12, alpha=0.45)
lo = min(y_test.min(), final_pred.min())
hi = max(y_test.max(), final_pred.max())
plt.plot([lo, hi], [lo, hi], linestyle="--")
plt.xlabel("Actual Delivery Time (hours)")
plt.ylabel("Predicted Delivery Time (hours)")
plt.title("Actual vs Predicted Delivery Time")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "actual_vs_predicted.png"), dpi=180)
plt.close()

residuals = y_test.to_numpy() - final_pred

plt.figure(figsize=(8, 5))
plt.scatter(final_pred, residuals, s=12, alpha=0.45)
plt.axhline(0, linestyle="--")
plt.xlabel("Predicted Delivery Time (hours)")
plt.ylabel("Residual (Actual - Predicted)")
plt.title("Residual Analysis")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "residual_analysis.png"), dpi=180)
plt.close()

# -----------------------------
# 12. Potential delay risk analysis
# -----------------------------
risk_count = int(test_results["potential_delay"].sum())
risk_pct = 100 * test_results["potential_delay"].mean()

print("\\nPotential delay risk:")
print("Risky deliveries:", risk_count)
print("Risk percentage:", round(risk_pct, 2))

for col in ["region", "delivery_partner", "vehicle_type", "weather_condition"]:
    group = (
        test_results.groupby(col)
        .agg(
            deliveries=("delivery_id", "size"),
            avg_predicted_time=("predicted_delivery_time_hours", "mean"),
            avg_expected_time=("expected_time_hours", "mean"),
            potential_delay_rate=("potential_delay", "mean"),
            avg_distance_km=("distance_km", "mean"),
            avg_cost=("delivery_cost", "mean")
        )
        .reset_index()
    )
    group["potential_delay_rate_pct"] = 100 * group["potential_delay_rate"]
    group = group.drop(columns="potential_delay_rate")
    group.to_csv(
        os.path.join(OUTPUT_DIR, f"{col}_risk_analysis.csv"), index=False
    )

# -----------------------------
# 13. Buffer references
# -----------------------------
absolute_errors = np.abs(residuals)
print("\\nModel error buffer references:")
print("MAE:", round(absolute_errors.mean(), 3), "hours")
print("90th percentile absolute error:", round(np.percentile(absolute_errors, 90), 3), "hours")
print("95th percentile absolute error:", round(np.percentile(absolute_errors, 95), 3), "hours")

# -----------------------------
# 14. Descriptive cost-time relationship
# -----------------------------
print("\\nDescriptive cost/time correlation:",
      round(df["delivery_time_hours"].corr(df["delivery_cost"]), 4))

# -----------------------------
# 15. Analytical scenario segments
# -----------------------------
test_results["cost_quartile"] = pd.qcut(
    test_results["delivery_cost"], 4,
    labels=["Q1 Lowest cost", "Q2", "Q3", "Q4 Highest cost"]
)

risk_mask = test_results["potential_delay"]
cost_mask = test_results["cost_quartile"] == "Q1 Lowest cost"

scenarios = pd.DataFrame([
    {
        "Scenario": "A - Current analytical baseline",
        "Deliveries": len(test_results),
        "Avg predicted h": test_results["predicted_delivery_time_hours"].mean(),
        "Avg expected h": test_results["expected_time_hours"].mean(),
        "Potential delay %": 100 * test_results["potential_delay"].mean(),
        "Avg cost": test_results["delivery_cost"].mean()
    },
    {
        "Scenario": "B - Risk-based priority segment",
        "Deliveries": int(risk_mask.sum()),
        "Avg predicted h": test_results.loc[risk_mask, "predicted_delivery_time_hours"].mean(),
        "Avg expected h": test_results.loc[risk_mask, "expected_time_hours"].mean(),
        "Potential delay %": 100.0,
        "Avg cost": test_results.loc[risk_mask, "delivery_cost"].mean()
    },
    {
        "Scenario": "C - Cost-conscious Q1 segment",
        "Deliveries": int(cost_mask.sum()),
        "Avg predicted h": test_results.loc[cost_mask, "predicted_delivery_time_hours"].mean(),
        "Avg expected h": test_results.loc[cost_mask, "expected_time_hours"].mean(),
        "Potential delay %": 100 * test_results.loc[cost_mask, "potential_delay"].mean(),
        "Avg cost": test_results.loc[cost_mask, "delivery_cost"].mean()
    }
])

scenarios.to_csv(os.path.join(OUTPUT_DIR, "optimization_scenarios.csv"), index=False)
print("\\nAnalytical scenarios:")
print(scenarios.round(3))

print("\\nCompleted. Outputs are in:", OUTPUT_DIR)
