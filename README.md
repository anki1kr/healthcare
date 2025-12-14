# Healthcare Data Analytics & Clinical Readmission Prediction

## Project Overview
This repository contains the complete analytical workflow, statistical modeling framework, and clinical decision-support pipeline developed during the **Healthcare Data Analyst Internship** (November 2025 – December 2025).

The primary clinical objective is to analyze inpatient trajectories across complex chronic disease cohorts (Heart Failure, Acute Myocardial Infarction, Type 2 Diabetes, Pneumonia, Sepsis), stratify 30-day all-cause unplanned readmission risk, and evaluate the operational and financial impact under the **CMS Hospital Readmissions Reduction Program (HRRP)**.

---

## Repository Structure

```
├── data/
│   └── hospital_admissions.csv                                        # 10,000 validated clinical encounter records
├── Week 1 - Healthcare Data Analysis Planning and Strategy/
│   └── Healthcare_Data_Analysis_Planning_and_Strategy.docx            # Project charter, scope, KPIs, and roadmap
├── Week 2 - Data Collection and Quality Assurance Planning/
│   └── Data_Collection_and_Quality_Assurance_Planning.docx            # Data sourcing, Kahn QA framework, HIPAA protocols
├── Week 3 - Data Visualization and Insights Communication/
│   └── Data_Visualization_and_Insights_Communication.docx             # Visual analytics strategy, wireframes, dashboard layout
├── Week 4 - Statistical Analysis and Predictive Modeling/
│   └── Statistical_Analysis_and_Predictive_Modeling.docx              # Hypothesis testing, XGBoost/LightGBM modeling, SHAP
├── Week 5 - Report Writing and Evidence-based Recommendations/
│   └── Report_Writing_and_Evidence_Based_Recommendations.docx         # Translational findings, HRRP financial ROI model
├── Week 6 - Comprehensive Project Integration and Self-Assessment/
│   └── Comprehensive_Project_Integration_and_Self_Assessment.docx     # End-to-end synthesis, self-assessment, best practices
├── requirements.txt                                                   # Python dependency specifications
└── README.md                                                          # Project documentation
```

---

## Weekly Milestone Breakdown

### Week 1: Strategic Planning and Healthcare Data Analysis Strategy
- Established clinical problem definition focusing on 30-day hospital readmissions and inpatient length of stay (LOS) variance.
- Defined enterprise KPIs: Readmission Rate reduction (-18%), ALOS optimization (-0.6 days), and HRRP penalty avoidance.
- Structured a 6-week operational roadmap, stakeholder engagement matrix, and preemptive clinical risk register.

### Week 2: Data Collection and Quality Assurance Planning
- Evaluated multi-source clinical repositories (MIMIC-IV, CMS Inpatient Quality, CDC NHANES).
- Implemented Kahn Harmonized Data Quality Framework (Completeness, Conformance, Plausibility, Temporal Consistency).
- Established automated data cleansing pipelines with K-Nearest Neighbors lab imputation and HIPAA Safe Harbor de-identification.

### Week 3: Data Visualization and Insights Communication
- Engineered clinical metric framework balancing quality (readmission rate, mortality) with capacity (bed occupancy, ED boarding).
- Developed 3-tier wireframe specifications: Executive C-Suite view, Service-Line Diagnostic matrix, and Bedside Transition worklist.
- Applied ColorBrewer color-vision deficiency safe palettes and action-oriented clinical alerts.

### Week 4: Statistical Analysis and Predictive Modeling
- Conducted hypothesis testing (Wilcoxon rank-sum, Chi-Square independence) identifying key physiological drivers.
- Formulated clinical risk indices: Polypharmacy Burden, Physiological Acuity, and Prior Utilization Velocity.
- Benchmarked 5 model architectures with 5-fold patient-level grouped cross-validation. Tuned XGBoost achieved **ROC-AUC of 0.835** and **PR-AUC of 0.771**.
- Integrated TreeSHAP for patient-level feature explanations and conducted demographic parity fairness auditing.

### Week 5: Report Writing and Evidence-based Recommendations
- Translated statistical patterns into 4 evidence-based operational pillars: Transitional Care Clinics, Bedside Med Reconciliation, 48-Hour Nursing Call Protocols, and Real-Time Risk Alerts.
- Built a financial ROI model projecting **$1.85 million in CMS penalty avoidance** and $3.2 million in total cost savings (370% ROI).

### Week 6: Comprehensive Project Integration and Self-Assessment
- Synthesized full analytical pipeline into a modular, production-ready inference script.
- Documented reflective intern self-assessment auditing technical growth, clinical data leakage mitigation, and ethical governance.
- Outlined a health informatics career development roadmap and best practices guide.

---

## Technical Environment and Setup

```bash
# Clone the repository
git clone https://github.com/anki1kr/Healthcare-Data-Analyst.git
cd Healthcare-Data-Analyst

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Author
- **Ankit Kumar** — Healthcare Data Analyst Intern
- Repository: [Healthcare-Data-Analyst](https://github.com/anki1kr/Healthcare-Data-Analyst)
- Contact: ankitkumar67930@gmail.com
