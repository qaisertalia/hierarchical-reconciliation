# =============================================================================
# utils/notebook_setup.py
#
# Paste this at the top of EVERY notebook — it handles the path issue once,
# so sys.path is always correct regardless of where Jupyter was launched.
#
# Usage:
#   from utils.notebook_setup import *
# =============================================================================

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

# ── Fix import path ───────────────────────────────────────────────────────────
# Walk up from this file until we find the project root
# (identified by the presence of config/ and utils/ folders)
def _find_project_root():
    current = os.path.abspath(os.path.dirname(__file__))
    for _ in range(5):                          # max 5 levels up
        current = os.path.dirname(current)
        if os.path.isdir(os.path.join(current, 'config')) and \
           os.path.isdir(os.path.join(current, 'utils')):
            return current
    raise RuntimeError(
        'Could not find project root. '
        'Make sure config/ and utils/ exist in your project folder.'
    )

_root = _find_project_root()
if _root not in sys.path:
    sys.path.insert(0, _root)

# ── Import config ─────────────────────────────────────────────────────────────
from config.settings import cfg, DATASET

# ── Confirm ───────────────────────────────────────────────────────────────────
print(f'Project root : {_root}')
print(f'Dataset      : {DATASET.upper()}')
print(f'Output dir   : {cfg["OUTPUT_DIR"]}')
