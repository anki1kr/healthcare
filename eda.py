"""
eda.py — Exploratory Data Analysis & Data Quality Assessment
Healthcare Data Analyst Internship | Weeks 2-3
Dataset: hospital_admissions.csv (n=10,000 clinical encounters)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_PATH = Path("data/hospital_admissions.csv")
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

# --- load ---
df = pd.read_csv(DATA_PATH)
print(f"Dataset: {df.shape[0]:,} rows × {df.shape[1]} columns\n")


# ── 1. Data Quality Audit (Kahn Framework) ─────────────────────────────────

print("=== DATA QUALITY AUDIT ===")

# completeness
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
print("\nMissing values:")
print(missing_pct[missing_pct > 0].to_string() if missing_pct.any() else "  None — dataset is complete")

# plausibility checks
assert df["age"].between(0, 120).all(), "Age out of range"
assert df["length_of_stay_days"].ge(0).all(), "Negative LOS"
assert df["readmitted_30d"].isin([0, 1]).all(), "Target not binary"
print("\nPlausibility checks: PASSED")

# distribution summary
print("\nNumerical summary:")
print(df.describe(include="number").T[["mean", "std", "min", "max"]].round(2).to_string())


# ── 2. Target Distribution ─────────────────────────────────────────────────

readmit_rate = df["readmitted_30d"].mean()
print(f"\n30-day readmission rate: {readmit_rate:.1%}")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# by diagnosis
dx_rates = (
    df.groupby("primary_diagnosis")["readmitted_30d"]
    .agg(["mean", "count"])
    .rename(columns={"mean": "readmit_rate", "count": "n"})
    .sort_values("readmit_rate", ascending=False)
)
dx_rates["readmit_rate"].plot(kind="bar", ax=axes[0], color="#c0392b", edgecolor="black")
axes[0].set_title("30-day Readmission Rate by Diagnosis")
axes[0].set_ylabel("Rate")
axes[0].set_xlabel("")
axes[0].tick_params(axis="x", rotation=30)
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))

# by age group
df["age_group"] = pd.cut(df["age"], bins=[17, 40, 60, 75, 120],
                          labels=["18-40", "41-60", "61-75", "76+"])
age_rates = df.groupby("age_group", observed=True)["readmitted_30d"].mean()
age_rates.plot(kind="bar", ax=axes[1], color="#2980b9", edgecolor="black")
axes[1].set_title("Readmission Rate by Age Group")
axes[1].set_ylabel("Rate")
axes[1].set_xlabel("")
axes[1].tick_params(axis="x", rotation=0)
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))

plt.tight_layout()
plt.savefig(OUT_DIR / "readmission_rates.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved -> outputs/readmission_rates.png")


# ── 3. Clinical Feature Distributions ─────────────────────────────────────

numeric_cols = [
    "age", "length_of_stay_days", "charlson_comorbidity_count",
    "prescribed_medication_count", "prior_inpatient_admissions_12m",
    "hba1c_level", "serum_creatinine_mg_dl", "systolic_blood_pressure",
]

fig, axes = plt.subplots(2, 4, figsize=(16, 7))
for ax, col in zip(axes.flatten(), numeric_cols):
    ax.hist(df[col].dropna(), bins=30, edgecolor="black", color="#7f8c8d")
    ax.set_title(col.replace("_", " ").title(), fontsize=9)
    ax.set_xlabel("")
plt.suptitle("Clinical Feature Distributions (n=10,000)", fontsize=12)
plt.tight_layout()
plt.savefig(OUT_DIR / "feature_distributions.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved -> outputs/feature_distributions.png")


# ── 4. Correlation with Readmission ────────────────────────────────────────

corr = df[numeric_cols + ["readmitted_30d"]].corr()["readmitted_30d"].drop("readmitted_30d").sort_values()

fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#c0392b" if v > 0 else "#2980b9" for v in corr]
corr.plot(kind="barh", ax=ax, color=colors, edgecolor="black")
ax.axvline(0, color="black", linewidth=0.8)
ax.set_title("Pearson Correlation with 30-day Readmission")
ax.set_xlabel("Correlation coefficient")
plt.tight_layout()
plt.savefig(OUT_DIR / "feature_correlation.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved -> outputs/feature_correlation.png")

print("\nEDA complete. All outputs in /outputs/")
