# Hierarchical Forecasting for Energy Systems

Reproducibility study examining the effect of hierarchical structure on forecast reconciliation accuracy for DSOs and aggregators.

Datasets: **London Climate & Household (LCL)** and **Combined Heat and Power (CHP)**

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/your-username/hierarchical-forecast.git
cd hierarchical-forecast

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your data (see Data section below)

# 4. Choose dataset — edit line 16 of config/settings.py
#    DATASET = 'lcl'   or   DATASET = 'chp'

# 5. Run notebooks in order
jupyter notebook notebooks/
```

---

## Before you run — three questions

Answer these to know which config values to check:

| Question | LCL answer | CHP answer |
|---|---|---|
| Voltage level? | Low (households) | Medium (CHPs) |
| Units in dataset? | ~5000 | ~50 |
| Metadata available? | Yes (Acorn, tariff) | Capacity only |

---

## Folder structure

```
hierarchical-forecast/
│
├── config/
│   ├── __init__.py
│   └── settings.py          ← EDIT THIS to switch datasets
│
├── notebooks/               ← run in order
│   ├── 01_ingest.ipynb
│   ├── 02_quality.ipynb
│   ├── 03_resample.ipynb
│   ├── 04_features.ipynb
│   ├── 05_forecast.ipynb
│   ├── 05b_crossval.ipynb   ← only run if forecast quality gate fails
│   ├── 06_coherency.ipynb
│   ├── 07_reconcile_flat.ipynb
│   ├── 08_metrics_flat.ipynb
│   ├── 09_clustering.ipynb
│   ├── 10_reconcile_structured.ipynb
│   ├── 11_metrics_structured.ipynb
│   └── 12_report.ipynb
│
├── utils/
│   ├── __init__.py
│   ├── notebook_setup.py    ← imported as first cell in every notebook
│   ├── cleaning.py          ← missing value functions
│   ├── metrics.py           ← MAPE, RMSE, sMAPE
│   └── plotting.py          ← shared chart functions
│
├── data/                    ← NOT committed to GitHub
│   ├── raw/
│   │   ├── lcl/             ← place LCL block CSVs + metadata + weather here
│   │   └── chp/             ← place chp_data.csv here
│   └── output/              ← parquets written by notebooks
│
├── results/                 ← NOT committed to GitHub
│   ├── figures/
│   └── reports/
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Data

Data is not included in this repository. Download and place files as follows:

**LCL**
- Source: https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households
- Place block CSVs in `data/raw/lcl/`
- Place `informations_households.csv` in `data/raw/lcl/`
- Place `weather_hourly_darksky.csv` in `data/raw/lcl/`

**CHP**
- Place `chp_data.csv` in `data/raw/chp/`

---

## Notebook pipeline

| # | Notebook | Input | Output |
|---|---|---|---|
| 01 | Ingest | raw CSVs | `raw_long_{dataset}.parquet` |
| 02 | Quality control | raw_long | `clean_long.parquet` |
| 03 | Window + resample | clean_long | `df_daily / hourly / native.parquet` |
| 04 | Feature engineering | df_daily | `df_features.parquet` |
| 05 | Forecast | df_features | `forecasts_individual / aggregate.parquet` |
| 05b | Cross-validation *(conditional)* | df_features | `cv_results.parquet`, updates forecasts |
| 06 | Coherency gap | forecasts | `coherency_gap.parquet` |
| 07 | Reconcile flat | forecasts | `reconciled_flat.parquet` |
| 08 | Metrics flat | reconciled_flat | `metrics_flat.parquet` |
| 09 | Clustering | df_features | `cluster_labels_*.parquet` |
| 10 | Reconcile structured | forecasts + cluster_labels | `reconciled_*.parquet` |
| 11 | Metrics structured | reconciled_* | `metrics_structured.parquet` |
| 12 | Report | all parquets | `dso_decision_report.json` |

---

## Research questions

1. How large is the coherency gap and does it scale with sample size?
2. Does flat MinT reconciliation improve or hurt individual unit accuracy?
3. Does a structured S matrix (Ward / metadata / random) improve accuracy vs flat MinT while keeping the gap at zero?
