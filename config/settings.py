# =============================================================================
# config/settings.py
#
# Change DATASET on line 16 to switch between LCL and CHP.
# Every notebook imports from here.
#
# Usage:
#   from config.settings import cfg, DATASET
# =============================================================================

# ── SWITCH DATASET HERE ───────────────────────────────────────────────────────
DATASET = 'lcl'     # 'lcl'  →  London smart meter households (consumption/demand)
                    # 'chp'  →  Combined Heat and Power plants (production/generation)


# =============================================================================
# LCL  —  London Low Carbon Households
# 30-min smart meter readings, ~2070 households, 2012–2014
# Variable: CONSUMPTION (demand) in kWh
# =============================================================================
LCL = dict(
    # Paths
    RAW_DIR          = 'data/raw/lcl/',
    RAW_FILE         = 'data/raw/lcl/elec_house.csv',
    METADATA_FILE    = 'data/raw/lcl/informations_households.csv',
    WEATHER_FILE     = 'data/raw/lcl/weather_hourly_darksky.csv',
    OUTPUT_DIR       = 'data/output_lcl_new/',

    # Column names
    ID_COL           = 'LCLid',
    TIME_COL         = 'timestamp',
    DEMAND_COL       = 'kWh',  # CHANGED: renamed from 'kWh' for clarity
    GROUP_COL        = 'file',
    WEATHER_COL      = 'temperature',
    RAW_TIME_COL     = 'tstp',
    RAW_DEMAND_COL   = None,
    META_COLS        = ['LCLid', 'Acorn_grouped', 'Acorn', 'stdorToU', 'file'],

    # Frequency and aggregation
    FREQ             = '30min',
    RESAMPLE_AGG     = 'sum',      # Sum kWh over time interval (energy accumulates)
    RESAMPLE_LABEL   = 'consumption (demand)',

    # Calendar
    HOLIDAY_COUNTRY  = 'UK',
    HOLIDAY_YEARS    = range(2012, 2015),

    # Quality control window
    WINDOW_START     = '2012-07-19 09:00:00',
    WINDOW_END       = '2014-02-19 00:00:00',
    MISSING_THRESH   = 0.20,
    NAN_STREAK_DAYS  = 7,
    INTERP_LIMIT     = 1,

    # Train/val/test split
    TRAIN_MONTHS     = 12,
    VAL_MONTHS       = 1,

    # Quality gates
    SMAPE_THRESHOLD  = 20.0,
    SMAPE_GATE       = 30.0,
    ZERO_THRESH      = 0.50,
    TEST_ZERO_THRESH = 0.50,
    DRIFT_THRESH     = 0.25,
    CV_FOLDS         = 5,

    # Models
    MODELS           = ['LR', 'LGBM'],

    # Features
    FEATURES_MANUAL  = ['year', 'weekday', 'consumption_kwh_lag24', 'consumption_kwh_lag168', 'temperature'],
    FEATURES         = None,

    # Hierarchy
    HIERARCHY_DEPTHS = [3, 4],

    # Sampling
    SAMPLE_SIZE      = 20,
    N_DRAWS          = 10,
)


# =============================================================================
# CHP  —  Combined Heat and Power plants
# Hourly MW production readings, ~82 plants, 2021–2023
# Variable: PRODUCTION (generation) in MW (power), stored as MWh (hourly energy)
# =============================================================================
CHP = dict(
    # Paths
    RAW_DIR              = 'data/raw/chp/',
    RAW_FILE             = 'data/raw/chp/chp_data.csv',
    METADATA_FILE        = None,
    WEATHER_FILE         = 'data/raw/chp/belgium_weather.csv',
    OUTPUT_DIR           = 'data/output_/new',

    # Column names
    ID_COL               = 'chp_id',
    TIME_COL             = 'timestamp',
    DEMAND_COL           = 'production_mwh',  # CHANGED: renamed from 'MWh' to clarify it's production
    GROUP_COL            = 'chp_id',
    WEATHER_COL          = 'temperature',    # CHANGED: was None, but Belgium weather is available
    RAW_TIME_COL         = 'Date',
    RAW_DEMAND_COL       = 'NCNR Production MW',
    RAW_FORECAST_COL     = 'NCNR Production Forecast IntraDay MW',
    RAW_CAPACITY_COL     = 'Installed Capacity NCNR MW',
    DROP_UNIT            = '1680',
    DATETIME_START       = '2021-01-01 00:00:00',
    DATETIME_END         = '2023-05-13 23:00:00',

    # Frequency and aggregation
    FREQ                 = 'h',
    RESAMPLE_AGG         = 'mean',     # Average MW over time interval (power rates average)
    RESAMPLE_LABEL       = 'production (generation)',

    # Calendar
    HOLIDAY_COUNTRY      = 'BE',
    HOLIDAY_YEARS        = range(2021, 2024),

    # Quality control
    WINDOW_START         = None,
    WINDOW_END           = None,
    MISSING_THRESH       = 0.20,
    NAN_STREAK_DAYS      = 7,
    INTERP_LIMIT         = 1,

    # Train/val/test split
    TRAIN_MONTHS         = 18,
    VAL_MONTHS           = 1,

    # Quality gates
    SMAPE_THRESHOLD      = 20.0,
    SMAPE_GATE           = 30.0,
    ZERO_THRESH          = 0.50,
    TEST_ZERO_THRESH     = 0.50,
    DRIFT_THRESH         = 0.25,
    CV_FOLDS             = 5,

    # Models
    MODELS               = ['LR', 'LGBM'],

    # Features
    FEATURES_MANUAL      = ['year', 'weekday', 'production_mwh_lag24', 'production_mwh_lag168', 'temperature'],
    FEATURES             = None,

    # Hierarchy
    HIERARCHY_DEPTHS     = [3, 4],

    # Sampling
    SAMPLE_SIZE          = 50,
    N_DRAWS              = 10,

    # Shutdown detection (CHP-specific)
    SHUTDOWN_THRESH      = 0.5,       # MW threshold below which unit is considered off
    SHUTDOWN_MIN_HOURS   = 3,         # Consecutive hours to trigger shutdown flag
)


# =============================================================================
# Active config — imported by all notebooks
# =============================================================================
if DATASET == 'lcl':
    cfg = LCL
elif DATASET == 'chp':
    cfg = CHP
else:
    raise ValueError(f"Unknown DATASET '{DATASET}'. Use 'lcl' or 'chp'.")
