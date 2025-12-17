"""
model.py — Predictive Modeling: 30-day Hospital Readmission Risk
Healthcare Data Analyst Internship | Week 4
Pipeline: feature engineering → XGBoost classifier → SHAP explainability → fairness audit
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score, average_precision_score, classification_report
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import shap
import warnings
warnings.filterwarnings("ignore")

DATA_PATH = Path("data/hospital_admissions.csv")
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

# ── 1. Load & Feature Engineering ─────────────────────────────────────────

df = pd.read_csv(DATA_PATH)

# polypharmacy burden (Week 4 clinical risk index)
df["polypharmacy_flag"] = (df["prescribed_medication_count"] >= 5).astype(int)

# physiological acuity index (composite)
df["physiological_acuity"] = (
    (df["serum_creatinine_mg_dl"] > 1.5).astype(int) +
    (df["hba1c_level"] > 7.5).astype(int) +
    (df["systolic_blood_pressure"] > 140).astype(int)
)

# prior utilization velocity
df["high_prior_use"] = (df["prior_inpatient_admissions_12m"] >= 2).astype(int)

# encode categoricals
for col in ["gender", "admission_type", "primary_diagnosis"]:
    df[col] = LabelEncoder().fit_transform(df[col].astype(str))

FEATURES = [
    "age", "gender", "admission_type", "primary_diagnosis",
    "length_of_stay_days", "charlson_comorbidity_count",
    "prescribed_medication_count", "prior_inpatient_admissions_12m",
    "hba1c_level", "serum_creatinine_mg_dl", "systolic_blood_pressure",
    "polypharmacy_flag", "physiological_acuity", "high_prior_use",
]

X = df[FEATURES]
y = df["readmitted_30d"]

print(f"Features: {len(FEATURES)} | Positive rate: {y.mean():.1%}\n")


# ── 2. Model Comparison (5-fold CV) ────────────────────────────────────────

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "XGBoost": XGBClassifier(
        n_estimators=300, max_depth=4, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8,
        use_label_encoder=False, eval_metric="logloss",
        random_state=42, verbosity=0
    ),
}

print("=== MODEL COMPARISON (5-fold CV ROC-AUC) ===")
best_model, best_score = None, 0
for name, clf in models.items():
    scores = cross_val_score(clf, X, y, cv=cv, scoring="roc_auc", n_jobs=-1)
    print(f"  {name:25s}  AUC = {scores.mean():.3f} ± {scores.std():.3f}")
    if scores.mean() > best_score:
        best_score = scores.mean()
        best_model = clf


# ── 3. Final XGBoost — full fit for SHAP ──────────────────────────────────

best_model.fit(X, y)
proba = best_model.predict_proba(X)[:, 1]
pred = (proba >= 0.5).astype(int)

print(f"\nFinal XGBoost (full train):")
print(f"  ROC-AUC  : {roc_auc_score(y, proba):.3f}")
print(f"  PR-AUC   : {average_precision_score(y, proba):.3f}")
print(f"\n{classification_report(y, pred, target_names=['No Readmit', 'Readmit'])}")


# ── 4. SHAP Feature Importance ─────────────────────────────────────────────
# ponytail: always use XGBoost for TreeExplainer; LR isn't a tree model

import matplotlib.pyplot as plt

xgb = models["XGBoost"]
xgb.fit(X, y)
explainer = shap.TreeExplainer(xgb)
shap_values = explainer.shap_values(X)

plt.figure(figsize=(9, 6))
shap.summary_plot(shap_values, X, plot_type="bar", show=False)
plt.title("SHAP Feature Importance — XGBoost Readmission Model")
plt.tight_layout()
plt.savefig(OUT_DIR / "shap_importance.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved -> outputs/shap_importance.png")


# ── 5. Demographic Fairness Audit ─────────────────────────────────────────

print("\n=== DEMOGRAPHIC PARITY AUDIT ===")
df["risk_score"] = proba
df["predicted"] = pred

# reload original gender string for audit
df_orig = pd.read_csv(DATA_PATH)
df["gender_label"] = df_orig["gender"]

for group_col in ["gender_label"]:
    grp = df.groupby(group_col).agg(
        n=("readmitted_30d", "count"),
        actual_rate=("readmitted_30d", "mean"),
        predicted_rate=("predicted", "mean"),
        mean_risk_score=("risk_score", "mean"),
    ).round(3)
    print(f"\nBy {group_col}:")
    print(grp.to_string())

print("\nModel pipeline complete.")
