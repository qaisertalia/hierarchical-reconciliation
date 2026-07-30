# Hierarchical Forecasting for Energy Systems

Reproducibility study examining the effect of hierarchical structure on forecast reconciliation accuracy for DSOs and aggregators.

Datasets: **London Climate & Household (LCL)** and **Combined Heat and Power (CHP)**

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/qaisertalia/hierarchical-reconciliation.git
cd hierarchical-reconciliation

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your data (see Data section below)

# 4. Choose dataset — edit line 12 of config/settings.py
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
hierarchical-reconciliation/
│
├── config/
│   ├── __init__.py
│   └── settings.py                        ← EDIT THIS to switch datasets
│
├── notebooks/                             ← run in order
│   ├── 01_ingest_corrected.ipynb
│   ├── 02_quality_updated.ipynb
│   ├── 03_resample_updated.ipynb
│   ├── 04_features_updated.ipynb
│   ├── 05_forecast_lcl_optimized.ipynb
│   ├── 05_forecast_chp_cleaned.ipynb
│   ├── 06_coherency_optimized.ipynb
│   ├── 07_reconcile_updated (1).ipynb
│   ├── 08_clustering_updated.ipynb
│   └── 08c_statistical_tests_fixed.ipynb
│
├── utils/
│   ├── __init__.py
│   └── notebook_setup.py                  ← imported as first cell in every notebook
│
├── data/                                  ← NOT committed to GitHub
│   ├── raw/
│   │   ├── lcl/                           ← place LCL block CSVs + metadata + weather here
│   │   └── chp/                           ← private dataset, not publicly available
│   └── output*/                           ← parquets written by notebooks
│
├── results/                               ← NOT committed to GitHub
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
- Private dataset — cannot be shared or redistributed. Not publicly downloadable.
- Anyone reproducing the CHP results needs their own access to equivalent data, placed in `data/raw/chp/` with the schema expected by `config/settings.py` (`CHP` block).

---

## Notebook pipeline

| # | Notebook | Input | Output |
|---|---|---|---|
| 01 | Ingest | raw CSVs | `raw_long_{dataset}.parquet` |
| 02 | Quality control | raw_long | `clean_long.parquet` |
| 03 | Window + resample | clean_long | `df_daily / hourly / native.parquet` |
| 04 | Feature engineering | df_daily | `df_features.parquet` |
| 05 | Forecast (LCL or CHP variant) | df_features | `forecasts_individual / aggregate.parquet` |
| 06 | Coherency gap | forecasts | `coherency_gap.parquet` |
| 07 | Reconcile | forecasts | `reconciled.parquet` |
| 08 | Clustering | df_features | `cluster_labels_*.parquet` |
| 08c | Statistical tests | reconciled + cluster_labels | test results |

---

## Research questions

1. **RQ1: Quantifying incoherence.** What is the magnitude of the coherency gap in real-world grid-connected systems, and how does it vary across forecasting approaches?
2. **RQ2: Mechanism of improvement.** How does hierarchy depth affect the redistribution of reconciliation corrections across aggregation levels, and why does this redistribution improve operational applicability?
3. **RQ3: Structure vs. method.** Does hierarchy depth or clustering algorithm choice drive reconciliation performance improvements, does this hold across both local and global forecasting models, and what design rules can we establish for practitioners?
